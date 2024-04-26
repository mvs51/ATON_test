from django.shortcuts import render

import pandas as pd
from urllib.request import urlopen


def index(request):
    template = 'index.html'
    return render(request, template, {})

def get_currency(request):
    template = 'currency.html'
    url = 'https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur=52148&bd=26&bm=3&by=2024&ed=26&em=4&ey=2024&x=28&y=8#archive'
    page = urlopen(url)
    html = page.read().decode("cp1251")

    res = pd.read_html(html, thousands=None, decimal=',')

    context = {
        'currency': res[1].to_html(classes='table table-bordered', index=False, justify='center')
    }
    return render(request, template, context)
