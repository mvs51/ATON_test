import os

import pandas as pd
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from currency.models import Currency
from .utils import (
    read_currency_rates,
    process_currencies,
    save_to_database,
    read_country_codes,
    process_country_codes
)


class CurrencyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_api.html'

    def get(self, request):
        queryset = Currency.objects.all()

        return Response({'currencies': queryset})
    
    def post(self, request):
        rates_html = read_currency_rates(
            request.POST.get('start_date'),
            request.POST.get('end_date'),
            request.POST.get('currency_name')
        )
        currencies = process_currencies(
            pd.read_html(rates_html, thousands=None, decimal=',')[1],
            request.POST.get('currency_name')
        )
        country_codes_html = read_country_codes()
        country_codes = process_country_codes(
            pd.read_html(country_codes_html, thousands=None, decimal=',')[0]
        )
        currencies = currencies.merge(
            country_codes, how='left', on='name_code'
        )
        save_to_database(currencies)
        context = {
            'currencies': currencies.to_html(
                classes='table table-bordered',
                index=False,
                justify='center')
        }
        return Response(context)