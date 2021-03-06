# Generated by Django 3.2.8 on 2022-04-18 20:42

from django.db import migrations, models
import django.db.models.expressions
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20220418_1754'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='timeoffrequest',
            constraint=models.CheckConstraint(check=models.Q(('start_date__gte', django.db.models.functions.datetime.Now()), ('start_date__lte', django.db.models.expressions.F('end_date'))), name='correct_datetime'),
        ),
    ]
