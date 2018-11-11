# Generated by Django 2.1 on 2018-11-11 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsse_api', '0030_auto_20181111_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditinspection',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeecommunityactivity',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='environmentalindicator',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthlyreport',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safetyactivity',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='created_on',
            field=models.DateField(default='2018-10-01'),
            preserve_default=False,
        ),
    ]
