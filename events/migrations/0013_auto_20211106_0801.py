# Generated by Django 3.2.8 on 2021-11-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_eventcustomer_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventstaff',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='eventstaff',
            name='total_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
