# Generated by Django 3.2.8 on 2021-11-28 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('square', '0003_square_other_tender_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='square',
            name='deposit_date',
        ),
        migrations.RemoveField(
            model_name='square',
            name='deposit_details',
        ),
        migrations.RemoveField(
            model_name='square',
            name='deposit_id',
        ),
        migrations.RemoveField(
            model_name='square',
            name='dining_option',
        ),
        migrations.RemoveField(
            model_name='square',
            name='discount_name',
        ),
        migrations.RemoveField(
            model_name='square',
            name='fee_fixed_rate',
        ),
        migrations.RemoveField(
            model_name='square',
            name='fee_percentage_rate',
        ),
        migrations.RemoveField(
            model_name='square',
            name='order_reference_id',
        ),
        migrations.RemoveField(
            model_name='square',
            name='refund_reason',
        ),
        migrations.RemoveField(
            model_name='square',
            name='transaction_status',
        ),
    ]