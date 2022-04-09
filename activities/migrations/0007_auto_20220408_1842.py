# Generated by Django 3.2.8 on 2022-04-08 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_activity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(default='Activity Time Entry', max_length=50),
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(choices=[('f', 'Artist Training'), ('c', 'Customer eXperience'), ('t', 'General Office Work')], default='c', max_length=1),
        ),
    ]
