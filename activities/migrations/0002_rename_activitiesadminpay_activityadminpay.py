# Generated by Django 3.2.8 on 2022-04-02 11:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActivitiesAdminPay',
            new_name='ActivityAdminPay',
        ),
    ]