import datetime
import re

from jija.serializers.exceptions import ValidationError


class Validator:
    @classmethod
    async def validate(cls, value, field):
        raise NotImplementedError()


class LengthMinValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if field.min_length and len(value) < field.min_length:
            raise ValidationError(f'Value must be longer that {field.min_length} symbols', value)

        return value


class LengthMaxValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if field.max_length and len(value) > field.max_length:
            raise ValidationError(f'Value must be shorter that {field.max_length} symbols', value)

        return value


class RegexValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if field.regex and not re.match(field.regex, value):
            raise ValidationError(f'Строка не соответствует шаблону', value)

        return value


class IntegerValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        try:
            return int(value)
        except ValueError:
            raise ValidationError('Value must be numeric', value)


class FloatValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        try:
            return float(value)
        except ValueError:
            raise ValidationError('Value must be numeric', value)


class RangeMinValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if field.min_value and value < field.min_value:
            raise ValidationError(f'Число должна быть больше либо равно {field.min_value}', value)

        return value


class RangeMaxValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if field.max_value and value > field.max_value:
            raise ValidationError(f'Число должно быть меньше либо равно {field.max_value}', value)

        return value


class DateValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Неверный формат', value)


class OptionsValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if value not in field.options:
            raise ValidationError(f'Недопустимое значение', value)

        return value


class SubclassValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if not issubclass(value, field.class_pattern):
            raise ValidationError(f'Value must be subclass of {field.class_pattern}, not {type(value)}', value)

        return value


class InstanceValidator(Validator):
    @classmethod
    async def validate(cls, value, field):
        if not isinstance(value, field.instance_pattern):
            raise ValidationError(f'Value must be instance of {field.instance_pattern}, not {type(value)}', value)

        return value
