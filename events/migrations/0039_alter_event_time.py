# Generated by Django 3.2.8 on 2021-11-14 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_auto_20211114_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(),
        ),
    ]