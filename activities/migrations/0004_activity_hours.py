# Generated by Django 3.2.8 on 2022-04-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_activity_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]
