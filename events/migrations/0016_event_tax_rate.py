# Generated by Django 3.2.8 on 2021-11-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20211106_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tax_rate',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=4),
        ),
    ]
