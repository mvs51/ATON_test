from datetime import datetime
from urllib import request, parse

import pandas as pd
import sqlite3


URL_RATES = 'https://www.finmarket.ru/currency/rates/?'
URL_COUNTRIES = 'https://www.iban.ru/currency-codes'

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
        start_date:str,
        end_date:str,
        cur:int
    ):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
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

    return page.read().decode("cp1251")


def process_currencies(df:pd.DataFrame, cur:str):
    currencies = df.rename(columns={
        'Дата': 'date',
        'Кол-во': 'quantity',
        'Курс': 'value',
        'Изменение': 'difference'
    })
    currencies['date']= pd.to_datetime(
        currencies['date'], format="%d.%m.%Y"
    )
    currencies['value'] = currencies['value']/currencies['quantity']
    currencies['name_code'] = CODES_MAPPING[int(cur)]
    return currencies.drop(columns=['difference', 'quantity'])


def save_to_database(df: pd.DataFrame):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    update_query = '''
        INSERT INTO currency (date, name, name_code, value)
        SELECT date, name, name_code, value
        FROM temp_table WHERE true
        ON CONFLICT(date, name_code)
        DO UPDATE SET value=EXCLUDED.value;
    '''
    df.to_sql('temp_table', con, if_exists='replace', index_label='id')
    cur.execute(update_query)
    con.commit()
    con.close()

def read_country_codes():
    page = request.urlopen(URL_COUNTRIES)
    return page.read().decode("utf-8")


def process_country_codes(df:pd.DataFrame):
    currency_codes = df.rename(columns={
        'Код': 'name_code',
        'Валюта': 'name',
    })
    currency_codes = currency_codes.drop_duplicates(
        subset=['name_code', 'name']
    )
    return currency_codes[['name_code', 'name']]
