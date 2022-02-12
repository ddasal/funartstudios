from django.db import models
from decimal import Decimal
# Create your models here.

class TransactionStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    ABANDONDED = 'a', 'Abandoned'
    COMPLETED = 'c', 'Completed'


class Square(models.Model):
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    time_zone = models.CharField(max_length=50)
    gross_sales = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    discounts = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    net_sales = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    gift_card_sales = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    tax = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    tip = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    partial_refunds = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    total_collected = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    source = models.CharField(max_length=50)
    card = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    card_entry_methods = models.CharField(max_length=50)
    cash = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    square_gift_card = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    other_tender = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    other_tender_type = models.CharField(max_length=50)
    other_tender_note = models.CharField(max_length=50)
    fees = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    net_total = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    payment_id = models.TextField()
    card_brand = models.CharField(max_length=50)
    pan_suffix = models.CharField(max_length=50)
    device_name = models.CharField(max_length=50)
    staff_name = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=50)
    details = models.TextField()
    description = models.TextField()
    event_type = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    customer_reference_id = models.CharField(max_length=50)
    device_nickname = models.CharField(max_length=50)
    taxable_sales = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, default=0.0)
    status = models.CharField(max_length=1, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)

    # def save(self, *args, **kwargs):
    #     if self.tax > 0:
    #         self.taxable_sales = Decimal(self.tax) / Decimal(0.81)
    #     super().save(*args, **kwargs)

    
