import inspect
import json
from typing import Union, Type

import aiohttp.http_websocket
from aiohttp import web

from jija import response, serializers, exceptions


class _ViewBase:
    def __init__(self, request: web.Request, path_params: web.UrlMappingMatchInfo):
        self.__request = request
        self.__path_params = path_params

    @property
    def request(self) -> web.Request:
        return self.__request

    @classmethod
    def get_methods(cls):
        raise NotImplementedError()

    @classmethod
    async def construct(cls, request: web.Request):
        view = cls(request, request.match_info)
        return await view.wrapper()

    async def wrapper(self):
        try:
            return await self.dispatch()

        except exceptions.ViewForceExit as exception:
            return exception.response

    async def dispatch(self):
        raise NotImplementedError()


class View(_ViewBase):
    methods = ('get', 'post', 'patch', 'put', 'delete')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__method = self.request.method.lower()
        self.__data: dict = {}

    @property
    def method(self) -> str:
        return self.__method

    @property
    def data(self) -> dict:
        return self.__data

    @classmethod
    def get_methods(cls):
        view_methods = []
        for method in cls.methods:
            if hasattr(cls, method):
                view_methods.append(method)

        return view_methods

    async def dispatch(self):
        await self.load_data()
        handler = getattr(self, self.method)
        return await self.run_handler(handler)

    async def load_data(self):
        self.__data = {
            **await self.parse_body(),
            **self.parse_path(),
            **self.parse_query()
        }

    async def parse_body(self) -> dict:
        if self.method != 'get':
            try:
                return await self.request.json()
            except json.JSONDecodeError:
                return {}

        return {}

    def parse_path(self) -> dict:
        return dict(self.request.match_info)

    def parse_query(self) -> dict:
        data = {}

        for key in set(self.request.query.keys()):
            value = self.request.query.getall(key)
            if len(value) == 1:
                value = value[0]

            data[key] = value

        return data

    async def run_handler(self, handler):
        if inspect.iscoroutinefunction(handler):
            return await handler()
        else:
            return handler()


class _SerializedViewMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        for method in cls.get_methods():
            handler = getattr(cls, method)
            cls.__annotate_serializers(handler)

        return cls

    @staticmethod
    def __annotate_serializers(handler):
        handler_serializers = {}
        for name, arg in inspect.signature(handler).parameters.items():
            if name == 'self':
                continue

            if issubclass(arg.annotation, serializers.Serializer):
                handler_serializers[name] = arg.annotation

        handler.__serializers__ = handler_serializers


class SerializedView(View, metaclass=_SerializedViewMeta):
    async def dispatch(self):
        try:
            return await super().dispatch()

        except serializers.SerializeError as error:
            return response.JsonResponse(error.serializer.errors, status=400)

    async def run_handler(self, handler):
        data = await self.in_serialize(handler.__serializers__)
        if inspect.iscoroutinefunction(handler):
            return await handler(**data)
        else:
            return handler(**data)

    async def in_serialize(
            self,
            handler_serializers: dict[str, Type[serializers.Serializer]]
    ) -> dict[str, serializers.Serializer]:

        data = {}
        for name, serializer_class in handler_serializers.items():
            serializer = serializer_class(self.data)
            await serializer.in_serialize()

            if not serializer.valid:
                raise serializers.SerializeError(serializer)

            data[name] = serializer

        return data


class DocMixin:
    pass


class WSView(_ViewBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ws = None

    @classmethod
    def get_methods(cls):
        return 'get',

    @property
    def ws(self) -> web.WebSocketResponse:
        return self.__ws

    async def dispatch(self):
        await self.on_connect()
        await self.process()
        return self.ws

    async def on_connect(self):
        self.__ws = web.WebSocketResponse()
        await self.ws.prepare(self.request)

    async def process(self):
        async for message in self.ws:
            message: aiohttp.http_websocket.WSMessage

            if message.type == web.WSMsgType.TEXT:
                await self.on_message(message.data)
            elif message.type == web.WSMsgType.ERROR:
                await self.on_error(message.data)

    async def on_message(self, message):
        pass

    async def on_error(self, error: str):
        await self.close(code=500, message=error, force=True)

    async def send(self, message: Union[dict, str, bytes]):
        if isinstance(message, dict):
            await self.ws.send_json(message)
        elif isinstance(message, bytes):
            await self.ws.send_bytes(message)
        else:
            await self.ws.send_str(message)

    async def close(self, code: int = 1000, message: Union[str, bytes, dict] = None, force=False):
        if isinstance(message, dict):
            message = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            message = message.encode('utf-8')

        await self.ws.close(code=code, message=message)
        if force is True:
            raise exceptions.ViewForceExit(self.ws)
