from django.db.models import ExpressionWrapper, IntegerField, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from app.filters import BankFilter
from app.serializers import BankSerializer
from app.models import MortgageOffer
from app.utils import get_monthly_payment


class BanksViewSet(viewsets.ModelViewSet):
    """
    API Endpoint
    """
    queryset = MortgageOffer.objects.all()
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BankFilter
    filterset_fields = ['price', 'term']
    ordering_fields = ['payment', 'rate_max', 'rate_min']

    def get_queryset(self, ):
        queryset = self.queryset
        req_params = self.request.query_params
        ordering = self.request.query_params.get('ordering')
        if ordering in ('payment', '-payment'):
            queryset = queryset.annotate(
                payment=ExpressionWrapper(
                    get_monthly_payment(req_params, F('rate_min')), output_field=IntegerField())).order_by(ordering)
        if ordering in ('rate_min', 'rate_max'):
            queryset = queryset.order_by(ordering)
        return queryset
