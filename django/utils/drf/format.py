from django.utils.dateparse import (
    parse_datetime,
)
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


def str_to_datetime(value):
    try:
        parsed = parse_datetime(value)
        if parsed is not None:
            return parsed
    except ValueError:
        raise exceptions.ValidationError(
            _('“%(value)s” value has the correct format '
              '(YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) '
              'but it is an invalid date/time.'),
            code='invalid_datetime',
            params={'value': value},
        )
