from django.db import models


class Currency(models.Model):
    date = models.DateField(blank=False)
    value = models.FloatField(blank=False)
    difference = models.FloatField()

    class Meta:
        db_table = 'currency_table'
        managed = False
