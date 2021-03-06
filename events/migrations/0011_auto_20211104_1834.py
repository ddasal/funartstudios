# Generated by Django 3.2.8 on 2021-11-04 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20211104_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstaff',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=3.5, max_digits=4),
        ),
        migrations.AlterField(
            model_name='eventstaff',
            name='role',
            field=models.CharField(choices=[('f', 'Floor Artist'), ('s', 'Stage Artist'), ('t', 'Team Member')], default='s', max_length=1),
        ),
    ]
