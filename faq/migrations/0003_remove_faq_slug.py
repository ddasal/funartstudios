# Generated by Django 3.2.8 on 2022-07-10 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20220522_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='slug',
        ),
    ]