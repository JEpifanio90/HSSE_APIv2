# Generated by Django 2.1 on 2018-08-18 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsse_api', '0025_auto_20180817_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
