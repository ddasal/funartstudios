from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q, Sum
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import DecimalField
from django.urls import reverse
from django.utils import timezone
from payroll.models import PayReport
import uuid
import pathlib

from products.models import Product, PurchaseItem
from royaltyreports.models import RoyaltyReport
from taxreports.models import TaxReport
from .utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save
from accounts.models import UserProfile, UserPay

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
    PAINTPOUR = 'p', 'Paint Pour Event'
    PWAP = 'w', 'Painting with a Purpose Event'
    RETAILONLY = 'r', 'Retail Only'
    STANDARD = 's', 'Standard Event'
    TAXFREE = 't', 'Other Tax Free Event'

class EventTax(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    tax_rate = models.DecimalField(decimal_places=3, max_digits=4, null=False, blank=False, default=0.000)
    start_date = models.DateField(null=False, blank=False, default=timezone.now)
    end_date = models.DateField(null=False, blank=False, default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class EventQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(eventstaff__user__first_name__icontains=query)  | Q(eventstaff__user__last_name__icontains=query)
        return self.filter(lookups).distinct()

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class EventStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    COMPLETED = 'c', 'Completed'

class Event(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    length = models.CharField(max_length=4, choices=EventLength.choices, default=EventLength.TWOHOUR)
    type = models.CharField(max_length=1, choices=EventType.choices, default=EventType.STANDARD)
    slug = models.SlugField(null=True, blank=True, unique=True)
    tax_rate = models.DecimalField(decimal_places=3, max_digits=4, null=False, blank=False, default=0.000)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='created')
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='updated')
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=1, choices=EventStatus.choices, default=EventStatus.PENDING)
    payroll_status = models.CharField(max_length=1, choices=EventStatus.choices, default=EventStatus.PENDING)
    royalty_report = models.ForeignKey(RoyaltyReport, on_delete=SET_NULL, null=True, blank=True)
    payroll_report = models.ForeignKey(PayReport, on_delete=SET_NULL, null=True, blank=True)
    tax_report = models.ForeignKey(TaxReport, on_delete=SET_NULL, null=True, blank=True)

    objects = EventManager()

    @property
    def name(self):
        return self.title

    @property
    def tax_rate_percentage(self):
        return self.tax_rate * 100

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

    def get_adminpay_children(self):
        return self.adminpay_set.all()

    def get_eventcustomer_children(self):
        return self.eventcustomer_set.all()

    def get_eventimage_children(self):
        return self.eventimages_set.all()

    def get_eventtip_children(self):
        return self.eventtip_set.all()

    def get_image_upload_url(self):
        return reverse("events:event-image-upload", kwargs={"parent_slug": self.slug})

    def save(self, *args, **kwargs):
        effective_tax_rate = list(EventTax.objects.values_list('tax_rate').filter(start_date__lte=self.date, end_date__gte=self.date))
        if self.type == 'i':
            self.tax_rate = 0.00
        elif self.type == 'p':
            self.tax_rate = effective_tax_rate[0][0]  
        elif self.type == 'w':
            self.tax_rate = 0.00 
        elif self.type == 'r':
            self.tax_rate = effective_tax_rate[0][0]  
        elif self.type == 's':
            self.tax_rate = effective_tax_rate[0][0]  
        elif self.type == 't':
            self.tax_rate = 0.00 
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

class PayStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    APPROVED = 'a', 'Approved'
    COMPLETED = 'c', 'Completed'

class EventStaff(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    role = models.CharField(max_length=1, choices=EventStaffRole.choices, default=EventStaffRole.STAGE)
    hours = models.DecimalField(decimal_places=2, max_digits=4, null=False, blank=False, default=0.00)
    rate = models.DecimalField(decimal_places=2, max_digits=4, default=0.00, null=False, blank=False)
    prepaint_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    hourly_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    tip_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    commission_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    total_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    prepaint_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='prepaint_product', default=1)
    prepaint_qty = models.IntegerField(default=0, null=True, blank=True)
    event_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='event_product', default=1)
    event_qty = models.IntegerField(default=0, null=True, blank=True)
    typical_hours = models.DecimalField(decimal_places=2, max_digits=4, null=False, blank=False, default=0.00)
    cost_factor = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=True, blank=True)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
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

    def save(self, *args, **kwargs):
        try:
            pay_rate = list(UserPay.objects.values_list('stage', 'floor', 'team', 'prepaint_single', 'prepaint_double').filter(user__user_id=self.user.id, start_date__lte=self.event.date, end_date__gte=self.event.date))
            if self.role == 's':
                self.rate = pay_rate[0][0]
                if self.prepaint_qty == 0:
                    self.prepaint_pay = Decimal(0.0)
                if self.prepaint_qty == 1:
                    self.prepaint_pay = pay_rate[0][3]
                elif self.prepaint_qty >= 2:
                    self.prepaint_pay = pay_rate[0][4]
            elif self.role == 'f':
                self.rate = pay_rate[0][1]
            elif self.role == 't':
                self.rate = pay_rate[0][2]
        except:
            pay_rate = Decimal(0.00)
            if self.role == 's':
                self.rate = pay_rate[0][0]
                if self.prepaint_qty == 0:
                    self.prepaint_pay = Decimal(0.0)
                if self.prepaint_qty == 1:
                    self.prepaint_pay = pay_rate[0][3]
                elif self.prepaint_qty >= 2:
                    self.prepaint_pay = pay_rate[0][4]
            elif self.role == 'f':
                self.rate = pay_rate[0][1]
            elif self.role == 't':
                self.rate = pay_rate[0][2]

        prepaint_cost_factor = Decimal(0.0)
        event_cost_factor = Decimal(0.0)

        if self.prepaint_qty > 0:
            temp_prepaint_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.prepaint_product, date__lte=self.event.date).order_by('-date').first())
            prepaint_cost_factor = Decimal(temp_prepaint_cost[0]) * self.prepaint_qty

        if self.event_qty > 0:
            temp_event_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.event_product, date__lte=self.event.date).order_by('-date').first())
            event_cost_factor = Decimal(temp_event_cost[0]) * self.event_qty

        self.cost_factor = Decimal(prepaint_cost_factor) + Decimal(event_cost_factor)

        event_length = Event.objects.get(id=self.event.id)
        self.typical_hours = Decimal(event_length.length) + Decimal(1.5)
        self.hourly_pay = Decimal(self.rate) * Decimal(self.hours)
        self.total_pay = Decimal(self.hourly_pay) + Decimal(self.prepaint_pay) + Decimal(self.tip_pay) + Decimal(self.commission_pay)
        self.date = event_length.date
        super().save(*args, **kwargs)

class EventTip(models.Model):
    event = models.ForeignKey(Event, on_delete=CASCADE)
    tip_amount = models.DecimalField(decimal_places=2, max_digits=6, default=0.00, null=False, blank=False)
    stage_split = models.DecimalField(decimal_places=2, max_digits=3, null=False, blank=False, default=0.70)
    floor_split = models.DecimalField(decimal_places=2, max_digits=3, null=False, blank=False, default=0.30)
    stage_amount = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, default=0.0)
    floor_amount = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, default=0.0)
    credit_fee = models.DecimalField(decimal_places=2, max_digits=2, null=False, blank=False, default=.03)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return self.event.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:eventtip-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:hx-eventtip-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.floor_split = 1 - self.stage_split
        self.stage_amount = Decimal(self.tip_amount) * (Decimal(1) - Decimal(self.credit_fee)) * Decimal(self.stage_split)
        self.floor_amount = Decimal(self.tip_amount) * (Decimal(1) - Decimal(self.credit_fee)) * Decimal(self.floor_split)
        super().save(*args, **kwargs)
 

class EventCustomerType(models.TextChoices):
    HOMEKIT = 'h', 'Twist at Home Kit(s)'
    POPINPAINT = 'p', 'Pop In and Paint(s)'
    RESERVATION = 'r', 'Event Reservation(s)'

class CustomerStatus(models.TextChoices):
    PENDING = 'p', 'Pending Processing'
    COMPLETED = 'c', 'Completed Processing'

class EventCustomer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=EventCustomerType.choices, default=EventCustomerType.RESERVATION)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0.0, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=CASCADE, null=False, blank=False, related_name='customer_product', default=1)
    per_customer_qty = models.IntegerField(default=1, null=False, blank=False)
    total_customer_qty = models.IntegerField(default=0, null=False, blank=False)
    subtotal_price = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=False, blank=False)
    cost_factor = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=True, blank=True)
    product_cost = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=True, blank=True)
    taxes = models.DecimalField(decimal_places=2, max_digits=5, default=0.0, null=False, blank=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=False, blank=False)
    status = models.CharField(max_length=1, choices=CustomerStatus.choices, default=CustomerStatus.PENDING)
    date = models.DateField(null=False, blank=False, default=timezone.now)
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

    def save(self, *args, **kwargs):
        self.total_customer_qty = self.per_customer_qty * self.quantity
        self.subtotal_price = self.quantity * self.price
        self.date = self.event.date
        if self.type == 'h':
            self.taxes = self.subtotal_price * self.event.tax_rate
            self.total_price = self.subtotal_price + self.taxes
            self.cost_factor = self.quantity * self.price
            try:
                product_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.event.date).order_by('-date').first())
                self.product_cost = product_cost[0] * self.total_customer_qty
            except:
                product_cost = Decimal(1.99)
                self.product_cost = product_cost * self.total_customer_qty

        elif self.type == 'p':
            self.taxes = self.subtotal_price * self.event.tax_rate
            self.total_price = self.subtotal_price + self.taxes
            self.cost_factor = self.quantity * self.price
            try:
                product_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.event.date).order_by('-date').first())
                self.product_cost = product_cost[0] * self.total_customer_qty
            except:
                product_cost = Decimal(1.99)
                self.product_cost = product_cost * self.total_customer_qty

        elif self.type == 'r':
            try:
                cost_factor = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.event.date).order_by('-date').first())
                self.cost_factor = cost_factor[0] * self.total_customer_qty
                self.product_cost = self.cost_factor
                self.taxes = self.cost_factor * self.event.tax_rate
            except:
                cost_factor = Decimal(1.99)
                self.cost_factor = cost_factor * self.total_customer_qty
                self.taxes = self.cost_factor * self.event.tax_rate

            self.total_price = self.subtotal_price
        super().save(*args, **kwargs)
    
def revent_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"events/{new_fname}{fpath.suffix}"


class EventImages(models.Model):
    event = models.ForeignKey(Event, on_delete=CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    upload = models.ImageField(upload_to=revent_image_upload_handler, height_field=None, width_field=None, max_length=100)

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:eventimage-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:hx-eventimage-update", kwargs=kwargs)



class AdminPay(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    admin_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    note = models.CharField(max_length=50, null=False, blank=False, default='Add Justification Note')
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.event.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:adminpay-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.event.slug,
            "id": self.id
        }
        return reverse("events:hx-adminpay-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        event_length = Event.objects.get(id=self.event.id)
        self.date = event_length.date
        super().save(*args, **kwargs)
