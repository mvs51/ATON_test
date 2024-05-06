import os
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from currency.models import Currency


class CurrencyView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_api.html'
    
    def get(self, request):
        queryset = Currency.objects.all()
        return Response({'currencies': queryset})