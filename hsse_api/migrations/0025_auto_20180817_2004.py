# Generated by Django 2.1 on 2018-08-18 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsse_api', '0024_auto_20180817_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='incident_date',
            field=models.DateField(),
        ),
    ]
