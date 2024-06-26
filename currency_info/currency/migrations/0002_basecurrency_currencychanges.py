# Generated by Django 3.2 on 2024-05-14 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('name_code', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('JPY', 'JPY'), ('TRY', 'TRY'), ('INR', 'INR'), ('CNY', 'CNY')], max_length=3)),
                ('value', models.FloatField()),
            ],
            options={
                'unique_together': {('date',)},
            },
        ),
        migrations.CreateModel(
            name='CurrencyChanges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.basecurrency')),
                ('date_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.currency')),
            ],
            options={
                'unique_together': {('date', 'date_currency')},
            },
        ),
    ]
