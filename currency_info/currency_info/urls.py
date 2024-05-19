from django.contrib import admin
from django.urls import path, include

from api.views import (
    CurrencyView, BaseCurrencyView, CurrencyChangesView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('currency.urls')),
    path('api/currency', CurrencyView.as_view(), name='currency'),
    path(
        'api/base_currency',
        BaseCurrencyView.as_view(),
        name='base_currency'
    ),
    path(
        'api/currency_changes',
        CurrencyChangesView.as_view(),
        name='currency_changes'
    )
]
