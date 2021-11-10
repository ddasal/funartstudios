# Generated by Django 3.2.8 on 2021-11-08 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20211106_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpay',
            name='stage',
            field=models.CharField(choices=[('p', 'Pending Processing'), ('c', 'Completed Processing')], default='p', max_length=1),
        ),
    ]