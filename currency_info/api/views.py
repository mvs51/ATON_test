import pandas as pd
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from currency.models import (
    Currency, BaseCurrency, CurrencyChanges
)
from .utils import (
    read_currency_rates,
    process_currencies,
    save_to_database,
    read_country_codes,
    process_country_codes,
    CODES_MAPPING,
)


class CurrencyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency.html'

    def get(self, request):
        queryset = Currency.objects.all()

        return Response({'currencies': queryset})
    
    def post(self, request):
        rates_html = read_currency_rates(
            request.POST.get('currency_name'),
            request.POST.get('start_date'),
            request.POST.get('end_date'),
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
        # save_to_database(currencies)
        for index, row in currencies.iterrows():
            Currency.objects.update_or_create(
                date=row['date'],
                name_code=row['name_code'],
                defaults={'value':row['value']}
            )

        for index, row in currencies.iterrows():
            if not CurrencyChanges.objects.filter(
                date=row['date'],
                date_currency=Currency.objects.get(
                    date=row['date'], name_code=row['name_code']
                ),
            ).exists():
                CurrencyChanges.objects.create(
                    date=row['date'],
                    date_currency=Currency.objects.get(
                        date=row['date'], name_code=row['name_code']
                    ),
                    base_currency=get_object_or_404(BaseCurrency, name_code=row['name_code'])
                )
        context = {
            'currencies': currencies.to_html(
                classes='table table-bordered',
                index=False,
                justify='center')
        }
        return Response(context)


class BaseCurrencyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'base_currency.html'

    def get(self, request):
        queryset = BaseCurrency.objects.all()

        return Response({'base_currencies': queryset})
    
    def post(self, request):
        date = request.POST.get('date')
        base_currencies = pd.DataFrame()
        for code in CODES_MAPPING:
            rates_html = read_currency_rates(code, date)
            currencies = process_currencies(
                pd.read_html(rates_html, thousands=None, decimal=',')[1],
                code
            )[:1]
            base_currencies = pd.concat(
                [base_currencies, currencies],
                ignore_index=True
            )
        
        country_codes_html = read_country_codes()
        country_codes = process_country_codes(
            pd.read_html(country_codes_html, thousands=None, decimal=',')[0]
        )
        base_currencies = base_currencies.merge(
            country_codes, how='left', on='name_code'
        )
        context = {
            'base_currencies': base_currencies.to_html(
                classes='table table-bordered',
                index=False,
                justify='center')
        }
        for index, row in base_currencies.iterrows():
            BaseCurrency.objects.update_or_create(
                name=row['name'],
                name_code=row['name_code'],
                defaults={'date':row['date'], 'value':row['value']}
            )
        return Response(context)


class CurrencyChangesView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_changes.html'

    def get(self, request):
        queryset = CurrencyChanges.objects.all()
    
        return Response({'currency_changes': queryset})