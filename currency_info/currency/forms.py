from django import forms


class Currency_requestForm(forms.Form):
    """Форма для запроса данных о курсе валют"""
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
