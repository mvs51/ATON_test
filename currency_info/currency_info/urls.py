from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import CurrencyView

router_v1 = routers.DefaultRouter()
# router_v1.register(r'currency', CurrencyView.as_view(), basename='currency')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('currency.urls')),
    path('api/currency', CurrencyView.as_view())
]
