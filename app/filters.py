import django_filters
from Tools.scripts.make_ctype import method
from django.db.models import F, IntegerField, ExpressionWrapper, FloatField

from app.models import MortgageOffer
from app.utils import get_monthly_payment


class BankFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name='price', method='price_filter', label='Цена недвижимости')
    term = django_filters.NumberFilter(field_name='term', method='term_filter', label='Срок Ипотеки')
    deposit = django_filters.NumberFilter(field_name='deposit', method='deposit_filter', label='Депозит')
    payment_min = django_filters.NumberFilter(field_name='payment_min', method='payment_min_filter',
                                              label='Ежемесячный платеж, ОТ')
    payment_max = django_filters.NumberFilter(field_name='payment_max', method='payment_max_filter',
                                              label='Ежемесячный платеж, ДО')

    class Meta:
        model = MortgageOffer
        fields = {
            'rate_max': ['lte'],
            'rate_min': ['gte'],
        }

    def price_filter(self, queryset, arg, value: int):
        if value and value > 0:
            queryset = queryset.filter(payment_min__lte=value, payment_max__gte=value)
        return queryset

    def term_filter(self, queryset, arg, value: int):
        if value and value > 0:
            queryset = queryset.filter(term_min__lte=value, term_max__gte=value)
        return queryset

    def deposit_filter(self, queryset, arg, value: int):
        if value and value > 0:
            queryset = queryset.filter(payment_min__lte=value, payment_max__gte=value)
        return queryset

    def payment_min_filter(self, queryset, arg, value: int):
        if value and value > 0:
            req_params = self.request.query_params
            queryset = queryset.annotate(
                payment=ExpressionWrapper(get_monthly_payment(req_params, F('rate_min')), output_field=FloatField()))
            queryset = queryset.filter(payment__gte=value)
        return queryset

    def payment_max_filter(self, queryset, arg, value: int):
        if value and value > 0:
            req_params = self.request.query_params
            queryset = queryset.annotate(
                payment=ExpressionWrapper(get_monthly_payment(req_params, F('rate_min')), output_field=FloatField()))
            queryset = queryset.filter(payment__lte=value)
        return queryset
