# Generated by Django 3.2.8 on 2021-11-06 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211106_0853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone_primary',
            new_name='phone_home',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone_secondary',
            new_name='phone_mobile',
        ),
    ]
