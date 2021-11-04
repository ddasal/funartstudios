from django.db import models

# Create your models here.

class ProductType(models.TextChoices):
    CANVAS = 'c', 'Canvas'
    GLASSWARE = 'g', 'Glassware'
    WOODBOARD = 'm', 'Wood Board (MDF)'
    WOODPLANK = 'p', 'Wood Plank'
    OTHER = 'o', 'Other'


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    type = models.CharField(max_length=4, choices=ProductType.choices, default=ProductType.CANVAS)
    low_alert_level = models.IntegerField(default=40, null=False, blank=False)

    class Meta:
        ordering = [('name'), ]

    def __str__(self):
       return self.name