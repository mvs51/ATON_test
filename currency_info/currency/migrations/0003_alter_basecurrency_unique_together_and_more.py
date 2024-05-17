# Generated by Django 4.2.13 on 2024-05-16 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_basecurrency_currencychanges'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='basecurrency',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='basecurrency',
            name='date',
            field=models.DateField(unique=True),
        ),
        migrations.DeleteModel(
            name='CurrencyChanges',
        ),
    ]