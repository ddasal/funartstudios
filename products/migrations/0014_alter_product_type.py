# Generated by Django 3.2.8 on 2021-12-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_purchaseorder_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('c', 'Canvas'), ('g', 'Glassware'), ('s', 'Screen'), ('m', 'Wood Board (MDF)'), ('p', 'Wood Plank'), ('o', 'Other'), ('r', 'Retail')], default='c', max_length=4),
        ),
    ]