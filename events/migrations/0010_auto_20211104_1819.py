# Generated by Django 3.2.8 on 2021-11-04 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20211104_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcustomer',
            options={'ordering': ['-type', '-quantity']},
        ),
        migrations.AlterModelOptions(
            name='eventstaff',
            options={'ordering': ['-event_qty']},
        ),
        migrations.AddField(
            model_name='eventcustomer',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='eventcustomer',
            name='type',
            field=models.CharField(choices=[('h', 'Twist at Home Kit(s)'), ('p', 'Pop In and Paint(s)'), ('r', 'Event Reservation(s)')], default='r', max_length=1),
        ),
    ]