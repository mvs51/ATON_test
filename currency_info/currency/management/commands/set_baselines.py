import pandas as pd
from django.core.management.base import BaseCommand

from currency.models import BaseCurrency
from api.utils import (
    read_currency_rates,
    process_currencies,
    read_country_codes,
    process_country_codes,
    CODES_MAPPING,
)


URL_RATES = 'https://www.finmarket.ru/currency/rates/?'
URL_COUNTRIES = 'https://www.iban.ru/currency-codes'
DATE = '2023-9-1'


class Command(BaseCommand):
    help = 'Creates initial base currency values'

    def handle(self, *args, **options):
        base_currencies = pd.DataFrame()
        for code in CODES_MAPPING:
            rates_html = read_currency_rates(code, DATE)
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
        for index, row in base_currencies.iterrows():
            BaseCurrency.objects.update_or_create(
                name=row['name'],
                name_code=row['name_code'],
                defaults={'date': row['date'], 'value': row['value']}
            )
