# Generated by Django 3.2.8 on 2021-12-03 22:09

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0050_rename_filename_eventimages_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventimages',
            name='upload',
            field=models.ImageField(upload_to=events.models.revent_image_upload_handler),
        ),
    ]
