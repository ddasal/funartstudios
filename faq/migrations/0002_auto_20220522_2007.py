# Generated by Django 3.2.8 on 2022-05-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
        ),
        migrations.AlterField(
            model_name='faq',
            name='category',
            field=models.CharField(choices=[('f', 'FAM'), ('a', 'FAS Admin'), ('g', 'General'), ('p', 'Pop-In & Paint'), ('r', 'Private Parties'), ('w', 'Painting with a Purpose'), ('s', 'Square'), ('t', 'Twist at Home Kits')], default='g', max_length=1),
        ),
    ]
