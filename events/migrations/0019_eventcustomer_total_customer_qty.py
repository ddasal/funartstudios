# Generated by Django 3.2.8 on 2021-11-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_eventcustomer_cost_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcustomer',
            name='total_customer_qty',
            field=models.IntegerField(default=0),
        ),
    ]