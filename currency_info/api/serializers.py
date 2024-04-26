from rest_framework import serializers

from currency.models import Currency


class CurrencySerializer(serializers.Serializer):
    class Meta:
            model = Currency
            fields = '__all__'