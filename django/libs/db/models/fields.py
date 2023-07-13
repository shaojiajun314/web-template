import re
from json import dumps, loads
from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import CharField, TextField, Field

# mobilephonenumber = re.compile((
#     r'^(\+?(?:0086|086|86))?((?:13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[013567'
#     r'8]|18[0-9]|19[89])(?:\d{8}))$'))
mobilephonenumber = re.compile((r'^1\d{10}$'))


def is_mobile_phone_number(value):
    if mobilephonenumber.match(value) is None:
        raise ValidationError('''手机号不合法''')


class PhoneField(CharField):
    default_validators = [is_mobile_phone_number,]




class EnumField(Field):
    description = _("enum")

    def __init__(self, enum_data=None, *args, **kwargs):
        if enum_data is None:
            enum_data = OrderedDict()
        self.enum = OrderedDict(enumerate(enum_data))
        self.reverse_enum = OrderedDict(
            zip(self.enum.values(), self.enum.keys()))
        kwargs["choices"] = [(k, v) for k, v in enum_data.items()]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["choices"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "smallint"

    def from_db_value(self, value, expression, connection):
        return self.enum.get(value)

    def to_python(self, value):
        return self.enum.get(value)

    def get_prep_value(self, value):
        if isinstance(value, str):
            value = self.reverse_enum.get(value)
        return super().get_prep_value(value)

    def value_from_object(self, obj):
        return self.enum.get(getattr(obj, self.attname))


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class JSONField(TextField):
    def get_prep_value(self, value):
        return dumps(value, default=set_default)

    def from_db_value(self, value, expression, connection):
        return loads(value)
