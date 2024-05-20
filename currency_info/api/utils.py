from datetime import datetime, timedelta
from urllib import request, parse
from io import StringIO

import pandas as pd


URL_RATES = 'https://www.finmarket.ru/currency/rates/?'
URL_COUNTRIES = 'https://www.iban.ru/currency-codes'
ROUND_DIGITS = 4
CODES_MAPPING = {
    52148: 'USD',
    52170: 'EUR',
    52146: 'GBP',
    52246: 'JPY',
    52158: 'TRY',
    52238: "INR",
    52207: 'CNY',
}


def read_currency_rates(
        cur: int,
        start_date: str,
        end_date: str = '',
):
    '''Function to parse page with currency data'''

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = start_date + timedelta(days=1)

    params = {
        'cur': cur,
        'pv': 1,
        'bd': start_date.day,
        'bm': start_date.month,
        'by': start_date.year,
        'ed': end_date.day,
        'em': end_date.month,
        'ey': end_date.year,
    }

    data = parse.urlencode(params)
    page = request.urlopen(f'{URL_RATES}{data}')

    return StringIO(page.read().decode("cp1251"))


def process_currencies(df: pd.DataFrame, cur: str):
    '''Function to process currency data'''

    currencies = df.rename(columns={
        'Дата': 'date',
        'Кол-во': 'quantity',
        'Курс': 'value',
        'Изменение': 'difference'
    })
    currencies['date'] = pd.to_datetime(
        currencies['date'], format="%d.%m.%Y"
    )
    currencies['date'] = currencies['date'].dt.date
    currencies['value'] = round(
        currencies['value']/currencies['quantity'], ROUND_DIGITS
    )
    currencies['name_code'] = CODES_MAPPING[int(cur)]
    return currencies.drop(columns=['difference', 'quantity'])


def read_country_codes():
    '''Function to parse page with countries and codes'''

    page = request.urlopen(URL_COUNTRIES)
    return StringIO(page.read().decode("utf-8"))


def process_country_codes(df: pd.DataFrame):
    '''Function to process countries and codes'''

    currency_codes = df.rename(columns={
        'Код': 'name_code',
        'Валюта': 'name',
    })
    currency_codes = currency_codes.drop_duplicates(
        subset=['name_code', 'name']
    )
    return currency_codes[['name_code', 'name']]
