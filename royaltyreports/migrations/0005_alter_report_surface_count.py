# Generated by Django 3.2.8 on 2021-11-10 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royaltyreports', '0004_report_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='surface_count',
            field=models.IntegerField(default=0),
        ),
    ]
