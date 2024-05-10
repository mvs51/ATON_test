from django.db import models


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
        db_table = 'currency'
        managed = False
        unique_together = [['date', 'name_code']]
