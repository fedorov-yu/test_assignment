from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from app.filters import get_monthly_payment
from app.models import MortgageOffer


class BankSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()

    class Meta:
        model = MortgageOffer
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=MortgageOffer.objects.all(),
                fields=(
                    'bank_name',
                    'term_min',
                    'term_max',
                    'rate_min',
                    'rate_max',
                    'payment_min',
                    'payment_max')
            )
        ]

    def validate_rate_max(self, value: int | float) -> int | float:
        if value < 0 or value >= 100:
            raise serializers.ValidationError(
                'Ставка по ипотеке может быть от 0 до 100 %'
            )
        return value

    def validate_term_max(self, value: int | float) -> int | float:
        if value < 0 or value >= 100:
            raise serializers.ValidationError(
                'Ипотека не может быть дольше жизни человека:('
            )
        return value

    def get_payment(self, instance) -> int:
        req_params = self.context.get('request').query_params
        rate = instance.rate_min
        return round(get_monthly_payment(req_params, rate))
