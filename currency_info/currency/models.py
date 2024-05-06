from django.db import models


class Currency(models.Model):
    date = models.DateField(blank=False)
    name = models.CharField(max_length=100)
    value = models.FloatField(blank=False)
    difference = models.FloatField()

    class Meta:
        db_table = 'currency'
        managed = False
