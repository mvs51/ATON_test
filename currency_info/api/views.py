from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import ApiVIew

from currency.models import Currency


class CurrencyView(ApiVIew):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'templates/currency_api.html'
    
    def get(self, request):
        queryset = Currency.objects.all()
        return Response({'currencies': queryset})