from django.db import models
from computedfields.models import ComputedFieldsModel, computed


NAME_CODES_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('JPY', 'JPY'),
    ('TRY', 'TRY'),
    ('INR', 'INR'),
    ('CNY', 'CNY'),
)


class Currency(models.Model):
    '''Model for the currency rates storage'''

    date = models.DateField('date', blank=False)
    name = models.CharField('name', max_length=100)
    name_code = models.CharField(
        'name code',
        blank=False,
        max_length=3,
        choices=NAME_CODES_CHOICES,
    )
    value = models.FloatField('currency value', blank=False)

    class Meta:
        verbose_name = 'currency'
        unique_together = [['date', 'name_code']]


class BaseCurrency(models.Model):
    '''Model for base parameters storage'''

    date = models.DateField('date', blank=False)
    name = models.CharField('name', max_length=100)
    name_code = models.CharField(
        'name_code',
        blank=False,
        max_length=3,
        choices=NAME_CODES_CHOICES,
        unique=True,
    )
    value = models.FloatField('currency value', blank=False)

    class Meta:
        verbose_name = 'base_currency'
        unique_together = [['date', 'name_code']]


class CurrencyChanges(ComputedFieldsModel):
    '''Model for currencies changes storage'''

    date = models.DateField('date', blank=False)
    date_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    base_currency = models.ForeignKey(
        BaseCurrency,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )

    @computed(
        models.FloatField('difference'),
        depends=[
            ('date_currency', ['value']),
            ('base_currency', ['value']),
        ]
    )
    def difference(self):
        date_currency = self.date_currency.value
        base_currency = self.base_currency.value
        value = (date_currency - base_currency)/base_currency*100
        return round(value, 2)

    @computed(
        models.CharField('name code', max_length=3),
        depends=[
            ('date_currency', ['name_code']),
        ]
    )
    def name_code(self):
        return self.date_currency.name_code

    class Meta:
        unique_together = [['date', 'date_currency']]
