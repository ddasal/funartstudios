# Generated by Django 3.2.8 on 2021-11-06 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_productpurchaseitem_purchaseitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='purchase_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.purchaseorder'),
        ),
    ]
