from django.db import models
from django.urls import reverse
from django.db.models import Q
from events.utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save

# Create your models here.

class ProductType(models.TextChoices):
    CANVAS = 'c', 'Canvas'
    GLASSWARE = 'g', 'Glassware'
    SCREEN = 's', 'Screen'
    WOODBOARD = 'm', 'Wood Board (MDF)'
    WOODPLANK = 'p', 'Wood Plank'
    OTHER = 'o', 'Other'


class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(name__icontains=query) #| Q(content__icontains=query)
        return self.filter(lookups)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    type = models.CharField(max_length=4, choices=ProductType.choices, default=ProductType.CANVAS)
    low_alert_level = models.IntegerField(default=40, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True, unique=True)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def title(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug" : self.slug})

    def get_hx_url(self):
        return reverse("products:hx-detail", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("products:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("products:delete", kwargs={"slug": self.slug})

    class Meta:
        ordering = [('type'), ('name'), ]

    def __str__(self):
       return self.name

def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(product_pre_save, sender=Product)

def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(product_post_save, sender=Product)
