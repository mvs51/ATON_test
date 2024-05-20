from io import BytesIO
import base64

import pandas as pd
import matplotlib
import seaborn as sns
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
    read_country_codes,
    process_country_codes,
    CODES_MAPPING,
)


class CurrencyView(APIView):
    '''View for the Currency model'''

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
        for index, row in currencies.iterrows():
            Currency.objects.update_or_create(
                date=row['date'],
                name_code=row['name_code'],
                defaults={'value': row['value'], 'name': row['name']}
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
                    base_currency=get_object_or_404(
                        BaseCurrency, name_code=row['name_code']
                    )
                )
        context = {
            'currencies': currencies.to_html(
                classes='table table-bordered',
                index=False,
                justify='center')
        }
        return Response(context)


class BaseCurrencyView(APIView):
    '''View for the BaseCurrency model'''
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
                defaults={'date': row['date'], 'value': row['value']}
            )
        return Response(context)


class CurrencyChangesView(APIView):
    '''View for the CurrencyChanges model'''
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_changes.html'

    def get(self, request):
        queryset = CurrencyChanges.objects.all()

        return Response({'currency_changes': queryset})

    def post(self, request):
        matplotlib.use('agg')
        df = pd.DataFrame.from_records(
            CurrencyChanges.objects.filter(
                date__gte=request.POST.get('start_date'),
                date__lte=request.POST.get('end_date')
            ).values()
        )
        if df.shape[0] == 0:
            return Response({'no_data': True})
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        ax = sns.lineplot(
            df,
            x='date',
            y='difference',
            hue='name_code',
            markers=True
        )
        ax.tick_params(axis='x', rotation=90)
        ax.xaxis.set_major_locator(
            matplotlib.dates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter('%Y-%m-%d')
        )
        buf = BytesIO()
        ax.figure.savefig(buf, format='png')
        encoded_figure = base64.b64encode(buf.getvalue()).decode('utf-8')
        return Response({'figure': encoded_figure})
