from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from events.utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your models here.

class ProductType(models.TextChoices):
    CANVAS = 'c', 'Canvas'
    CERAMIC = 'm', 'Ceramic'
    GLASSWARE = 'g', 'Glassware'
    SCREEN = 's', 'Screen'
    WOODBOARD = 'm', 'Wood Board (MDF)'
    WOODPLANK = 'p', 'Wood Plank'
    OTHER = 'o', 'Other'
    RETAIL = 'r', 'Retail'


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
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    @property
    def title(self):
        return self.name

    def total_received_each(self):
        temp_received_each = [int(each.received_quantity) for each in PurchaseItem.objects.filter(product=self.id)]
        return sum(temp_received_each)

    def total_received_all(self):
        temp_received_all = [int(each.received_quantity) for each in PurchaseItem.objects.all()]
        return sum(temp_received_all)

    def total_purchased_each(self):
        temp_purchased_each = [int(each.purchased_quantity) for each in PurchaseItem.objects.filter(product=self.id)]
        return sum(temp_purchased_each)

    def total_purchased_all(self):
        temp_purchased_all = [int(each.purchased_quantity) for each in PurchaseItem.objects.all()]
        return sum(temp_purchased_all)

    def get_pi_list(self):
        temp_pi_list = PurchaseItem.objects.filter(product=self.id)
        return temp_pi_list

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

class Suppliers(models.TextChoices):
    THIRTEENTWENTYONECREATIVE = '3', '1320 Creative'
    ARTBOARDSDIRECT = 'b', 'Art Boards Direct'
    ARTDISTRIBUTORS = 'a', 'Art Supply Distributors'
    DIVERSEWOOD = 'd', 'Diverse Woodworking'
    CHESAPEAKE = 'c', 'Chesapeake Ceramics'
    HOBBYLOBBY = 'h', 'Hobby Lobby'
    INVENTORYADJUSTMENT = 'i', 'Inventory Adjustment'
    PGDUNN = 'p', 'P. Graham Dunn'
    TDART = 't', 'TD Art Supply'
    OTHER = 'o', 'Other'

class PurchaseOrder(models.Model):
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    supplier = models.CharField(max_length=1, choices=Suppliers.choices, default=Suppliers.TDART)
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("products:po-detail", kwargs={"id" : self.id})

    def get_hx_url(self):
        return reverse("products:hx-po-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("products:po-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("products:po-delete", kwargs={"id": self.id})

    def get_purchaseitem_children(self):
        return self.purchaseitem_set.all()



class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    price_each = models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False, default=0.00)
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    purchased_quantity = models.IntegerField(null=False, blank=False, default=0)
    received_quantity = models.IntegerField(null=False, blank=False, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.date = self.purchase_order.date
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.purchase_order.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_id": self.purchase_order.id,
            "id": self.id
        }
        return reverse("products:po-item-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_id": self.purchase_order.id,
            "id": self.id
        }
        return reverse("products:hx-po-item-update", kwargs=kwargs)