# Generated by Django 3.2.8 on 2022-04-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_rename_typicalschedule_typical'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typical',
            name='notes',
            field=models.TextField(blank=True, default='I prefer to work X events per week.  I may be able to cover some last minute private parties or emergency coverages. Just ask.', null=True),
        ),
    ]
