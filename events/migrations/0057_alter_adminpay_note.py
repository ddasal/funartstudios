# Generated by Django 3.2.8 on 2022-01-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0056_adminpay_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminpay',
            name='note',
            field=models.CharField(default='Add Justification Note', max_length=50),
        ),
    ]