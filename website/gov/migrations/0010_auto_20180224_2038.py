# Generated by Django 2.0.2 on 2018-02-24 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gov', '0009_auto_20180224_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='current_rent',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='lease_years',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='property_address4',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
