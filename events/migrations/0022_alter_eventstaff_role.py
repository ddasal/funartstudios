# Generated by Django 3.2.8 on 2021-11-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_remove_eventstaff_total_staff_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstaff',
            name='role',
            field=models.CharField(choices=[('p', 'Pending Processing'), ('c', 'Completed Processing')], default='p', max_length=1),
        ),
    ]