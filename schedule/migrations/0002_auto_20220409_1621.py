# Generated by Django 3.2.8 on 2022-04-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='typicalschedule',
            name='friday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='monday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='saturday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='sunday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='thursday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='tuesday',
            field=models.CharField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='typicalschedule',
            name='wednesday',
            field=models.CharField(default=0, max_length=1),
        ),
    ]
