# Generated by Django 2.1 on 2018-11-11 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hsse_api', '0029_auto_20181020_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correctiveaction',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='correctiveaction',
            name='ehhs_leader',
        ),
        migrations.RemoveField(
            model_name='correctiveaction',
            name='manager',
        ),
        migrations.RemoveField(
            model_name='correctiveaction',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='environmentalindicator',
            name='month_created',
        ),
        migrations.RemoveField(
            model_name='environmentalindicator',
            name='year_created',
        ),
        migrations.RemoveField(
            model_name='monthlyreport',
            name='month_created',
        ),
        migrations.RemoveField(
            model_name='monthlyreport',
            name='year_created',
        ),
        migrations.RemoveField(
            model_name='report',
            name='month_created',
        ),
        migrations.RemoveField(
            model_name='report',
            name='year_created',
        ),
        migrations.DeleteModel(
            name='CorrectiveAction',
        ),
    ]
