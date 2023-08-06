from jija import response
from jija.contrib.swagger import processor


async def swagger_view(request):
    doc_processor = processor.DocsProcessor(request.app)
    return response.JsonResponse(data=await doc_processor.create_json())
