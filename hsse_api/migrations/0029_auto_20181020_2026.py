# Generated by Django 2.1 on 2018-10-21 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsse_api', '0028_auto_20181013_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('OV', 'Overdue'), ('CL', 'Closed'), ('IP', 'In progress'), ('O', 'Open')], default='O', max_length=11),
        ),
        migrations.AddField(
            model_name='user',
            name='contractor',
            field=models.BooleanField(default=False),
        ),
    ]
