# Generated by Django 3.2.8 on 2022-03-28 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0057_alter_adminpay_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcustomer',
            name='type',
            field=models.CharField(choices=[('h', 'Twist at Home Kit(s) / Pop-In & Paint'), ('r', 'Event Reservation(s)')], default='r', max_length=1),
        ),
    ]
