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
    date = models.DateField(blank=False)
    name = models.CharField(max_length=100)
    name_code = models.CharField(
        blank=False,
        max_length=3,
        choices=NAME_CODES_CHOICES,
    )
    value = models.FloatField(blank=False)

    class Meta:
        # db_table = 'currency'
        # managed = False
        unique_together = [['date', 'name_code']]


class BaseCurrency(models.Model):
    date = models.DateField(blank=False, unique=True)
    name = models.CharField(max_length=100)
    name_code = models.CharField(
        blank=False,
        max_length=3,
        choices=NAME_CODES_CHOICES,
    )
    value = models.FloatField(blank=False)


class CurrencyChanges(ComputedFieldsModel):
    date = models.DateField(blank=False)
    date_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )
    base_currency=models.ForeignKey(
        BaseCurrency,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [['date', 'date_currency']]
    
    @computed(
        models.FloatField(),
        depends=[
            ('self', ['name']),
            ('date_currency', ['value']),
            ('base_currency', ['value']),
        ]
    )
    def difference(self):
        return self.date_currency.value - self.base_currency.value
    
    @computed(
        models.FloatField(),
        depends=[
            ('self', ['name']),
            ('date_currency', ['name_code']),
        ]
    )
    def name_code(self):
        return self.date_currency.name_code


# class BaselineParams(models.Model):
#     date = models.DateField(blank=False)
