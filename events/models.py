from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DecimalField
from django.urls import reverse
from django.utils import timezone

from products.models import Product
from .utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save

User = settings.AUTH_USER_MODEL


class EventLength(models.TextChoices):
    HALFHOUR = 0.5, '1/2 Hour'
    ONEHOUR = 1.0, '1 Hour'
    ONEANDHALFHOUR = 1.5, '1 1/2 Hour'
    TWOHOUR = 2.0, '2 Hour'
    TWOANDHALFHOUR = 2.5, '2 1/2 Hour'
    THREEHOUR = 3.0, '3 Hour'
    THREEANDHALFHOUR = 3.5, '3 1/2 Hour'
    FOURFHOUR = 4.0, '4 Hour'
    OTHER = 0.0, 'Other'

class EventType(models.TextChoices):
    INTERNAL = 'i', 'Internal Event'
    PWAP = 'c', 'Painting with a Purpose Event'
    STANDARD = 's', 'Standard Event'
    PAINTPOUR = 'p', 'Paint Pour Event'
    TAXFREE = 't', 'Other Tax Free Event'

class EventQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(eventstaff__user__first_name__icontains=query)  | Q(eventstaff__user__last_name__icontains=query)
        return self.filter(lookups)

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Event(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    length = models.CharField(max_length=4, choices=EventLength.choices, default=EventLength.TWOHOUR)
    type = models.CharField(max_length=1, choices=EventType.choices, default=EventType.STANDARD)
    slug = models.SlugField(null=True, blank=True, unique=True)
    credit_tips =models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False, default=0.00)
    credit_tips_reduced =models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = EventManager()

    @property
    def name(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug" : self.slug})

    def get_hx_url(self):
        return reverse("events:hx-detail", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("events:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("events:delete", kwargs={"slug": self.slug})

    def get_eventstaff_children(self):
        return self.eventstaff_set.all()

    def get_eventcustomer_children(self):
        return self.eventcustomer_set.all()

    def save(self, *args, **kwargs):
        self.credit_tips_reduced = self.credit_tips * Decimal(.97)
        super().save(*args, **kwargs)

def event_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(event_pre_save, sender=Event)

def event_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(event_post_save, sender=Event)

class EventStaffRole(models.TextChoices):
    FLOOR = 'f', 'Floor Artist'
    STAGE = 's', 'Stage Artist'
    TEAM = 't', 'Team Member'

class EventStaff(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    role = models.CharField(max_length=1, choices=EventStaffRole.choices, default=EventStaffRole.STAGE)
    hours = models.DecimalField(decimal_places=2, max_digits=4, null=False, blank=False, default=3.5)
    prepaint_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='prepaint_product', default=5)
    prepaint_qty = models.IntegerField(default=0, null=True, blank=True)
    event_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='event_product', default=5)
    event_qty = models.IntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.event.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:eventstaff-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:hx-eventstaff-update", kwargs=kwargs)

    class Meta:
        ordering = [('-event_qty'), ]

    # def __str__(self):
    #    return self.user
       
class EventCustomerType(models.TextChoices):
    HOMEKIT = 'h', 'Twist at Home Kit(s)'
    POPINPAINT = 'p', 'Pop In and Paint(s)'
    RESERVATION = 'r', 'Event Reservation(s)'

class EventCustomer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=EventCustomerType.choices, default=EventCustomerType.RESERVATION)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0.0, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=CASCADE, null=False, blank=False, related_name='customer_product', default=5)
    per_customer_qty = models.IntegerField(default=1, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [('-type'),('-quantity'), ]

    def get_absolute_url(self):
        return self.event.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:eventcustomer-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:hx-eventcustomer-update", kwargs=kwargs)
