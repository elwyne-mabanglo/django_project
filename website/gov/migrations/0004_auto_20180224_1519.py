# Generated by Django 2.0.2 on 2018-02-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gov', '0003_auto_20180224_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='lease_end_date',
            field=models.DateField(verbose_name='lease end date'),
        ),
        migrations.AlterField(
            model_name='data',
            name='lease_start_date',
            field=models.DateField(verbose_name='lease start date'),
        ),
    ]
