from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('currency_info/', views.get_currency, name='currency_info')
]