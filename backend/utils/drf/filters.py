from rest_framework.filters import BaseFilterBackend
from .format import str_to_datetime
from django_filters.filters import BaseInFilter, UUIDFilter, NumberFilter
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DateTimeFilterSet(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_created_gte_str = request.query_params.get('date_created_gte')
        date_created_lte_str = request.query_params.get('date_created_lte')
        if date_created_gte_str:
            date_created_gte = str_to_datetime(date_created_gte_str)
            if not date_created_gte:
                raise ValidationError(
                    _(f'{date_created_gte_str} value has the correct format '
                      '(YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) '
                      'but it is an invalid date/time.')
                  )
            queryset = queryset.filter(date_created__gte=date_created_gte)
        if date_created_lte_str:
            date_created_lte = str_to_datetime(date_created_lte_str)
            if not date_created_lte:
                raise ValidationError(
                    _(f'{date_created_lte_str} value has the correct format '
                      '(YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) '
                      'but it is an invalid date/time.')
                  )
            queryset = queryset.filter(date_created__lte=date_created_lte)
        return queryset


class UUIDInFilter(BaseInFilter, UUIDFilter):
    pass

class IdInFilter(BaseInFilter, NumberFilter):
    pass
