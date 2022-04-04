from secrets import choice
from django.db import models

# Create your models here.
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q, Sum
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import DecimalField
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from payroll.models import PayReport
import uuid
import pathlib

from products.models import Product, PurchaseItem
from royaltyreports.models import RoyaltyReport
from taxreports.models import TaxReport
from events.utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save
from accounts.models import UserProfile, UserPay
from events.models import EventTax

User = settings.AUTH_USER_MODEL

class WorkType(models.TextChoices): 
    ARTIST = 'f', 'Artist Training'
    CUSTOMER = 'c', 'Customer eXperience'
    OFFICE = 't', 'General Office Work'


class WorkQuerySet(models.QuerySet): 
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(activitystaff__user__first_name__icontains=query)  | Q(activitystaff__user__last_name__icontains=query)
        return self.filter(lookups).distinct()

class WorkManager(models.Manager): 
    def get_queryset(self):
        return WorkQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class WorkStatus(models.TextChoices): 
    PENDING = 'p', 'Pending'
    COMPLETED = 'c', 'Completed'

class Activity(models.Model): 
    title = models.CharField(max_length=50, null=False, blank=False, default='Activity Time Entry')
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    hours = models.DecimalField(decimal_places=2, max_digits=4, null=False, blank=False, default=0.00)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    type = models.CharField(max_length=1, choices=WorkType.choices, default=WorkType.CUSTOMER)
    slug = models.SlugField(null=True, blank=True, unique=True)
    tax_rate = models.DecimalField(decimal_places=3, max_digits=4, null=False, blank=False, default=0.000)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='activity_created_by')
    updated_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='activity_updated_by')
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=1, choices=WorkStatus.choices, default=WorkStatus.PENDING)
    payroll_status = models.CharField(max_length=1, choices=WorkStatus.choices, default=WorkStatus.PENDING)
    royalty_report = models.ForeignKey(RoyaltyReport, on_delete=SET_NULL, null=True, blank=True)
    payroll_report = models.ForeignKey(PayReport, on_delete=SET_NULL, null=True, blank=True)
    tax_report = models.ForeignKey(TaxReport, on_delete=SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    objects = WorkManager()

    @property
    def name(self):
        return self.title

    @property
    def tax_rate_percentage(self):
        return self.tax_rate * 100

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("activities:detail", kwargs={"slug" : self.slug})

    def get_hx_url(self):
        return reverse("activities:hx-detail", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("activities:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("activities:delete", kwargs={"slug": self.slug})

    def get_activitiesstaff_children(self):
        return self.activitystaff_set.all()

    def get_activitiesadminpay_children(self):
        return self.activityadminpay_set.all()

    def get_activitiescustomer_children(self):
        return self.activitycustomer_set.all()

    def get_activitiesimage_children(self):
        return self.activityimages_set.all()

    def get_activitiestip_children(self):
        return self.activitytip_set.all()

    def get_image_upload_url(self):
        return reverse("activities:activities-image-upload", kwargs={"parent_slug": self.slug})

    def save(self, *args, **kwargs):
        title_options = [x[1] for x in WorkType.choices]
        effective_tax_rate = list(EventTax.objects.values_list('tax_rate').filter(start_date__lte=self.date, end_date__gte=self.date))
        if self.type == 'f':
            self.tax_rate = effective_tax_rate[0][0]  
            self.title = title_options[0]
        elif self.type == 't':
            self.tax_rate = effective_tax_rate[0][0]  
            self.title = title_options[2]
        elif self.type == 'c':
            self.tax_rate = effective_tax_rate[0][0]  
            self.title = title_options[1]
        try:
            child = ActivityStaff.objects.get(activity=self.id)
            if child:
                child.hours = self.hours
                child.save()
        except:
            pass
        super().save(*args, **kwargs)


def activity_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(activity_pre_save, sender=Activity)

def activity_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(activity_post_save, sender=Activity)

class ActivityStaffRole(models.TextChoices):
    FLOOR = 'f', 'Floor Artist'
    # STAGE = 's', 'Stage Artist'
    TEAM = 't', 'Team Member'
    CUSTOMER = 'c', 'Customer eXperience'

class PayStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    APPROVED = 'a', 'Approved'
    COMPLETED = 'c', 'Completed'

class ActivityStaff(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    role = models.CharField(max_length=1, choices=ActivityStaffRole.choices, default=ActivityStaffRole.CUSTOMER)
    hours = models.DecimalField(decimal_places=2, max_digits=4, null=False, blank=False, default=0.00)
    rate = models.DecimalField(decimal_places=2, max_digits=4, default=0.00, null=False, blank=False)
    prepaint_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    hourly_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    tip_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    commission_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    total_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    prepaint_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='activity_prepaint_product', default=1)
    prepaint_qty = models.IntegerField(default=0, null=True, blank=True)
    activity_product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True, related_name='activity_product', default=1)
    activity_qty = models.IntegerField(default=0, null=True, blank=True)
    cost_factor = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, null=True, blank=True)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.activity.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:activitystaff-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:hx-activitystaff-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        try:
            pay_rate = list(UserPay.objects.values_list('stage', 'floor', 'team', 'prepaint_single', 'prepaint_double', 'customer_experience').filter(user__user_id=self.user.id, start_date__lte=self.activity.date, end_date__gte=self.activity.date))
            if self.role == 'c':
                self.rate = pay_rate[0][5]
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
            if self.role == 'c':
                self.rate = pay_rate[0][5]
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
        activity_cost_factor = Decimal(0.0)

        if self.prepaint_qty > 0:
            temp_prepaint_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.prepaint_product, date__lte=self.activity.date).order_by('-date').first())
            prepaint_cost_factor = Decimal(temp_prepaint_cost[0]) * self.prepaint_qty

        if self.activity_qty > 0:
            temp_activity_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.activity_product, date__lte=self.activity.date).order_by('-date').first())
            activity_cost_factor = Decimal(temp_activity_cost[0]) * self.activity_qty

        self.cost_factor = Decimal(prepaint_cost_factor) + Decimal(activity_cost_factor)

        self.hourly_pay = Decimal(self.rate) * Decimal(self.hours)
        self.total_pay = Decimal(self.hourly_pay) + Decimal(self.prepaint_pay) + Decimal(self.tip_pay) + Decimal(self.commission_pay)
        super().save(*args, **kwargs)

@receiver(post_save, sender=Activity)
def create_activity_staff(sender, instance, created, **kwargs):
    if created:
        ActivityStaff.objects.create(activity=instance, role=instance.type, hours=instance.hours, user=instance.user)


class ActivityTip(models.Model):
    activity = models.ForeignKey(Activity, on_delete=CASCADE)
    tip_amount = models.DecimalField(decimal_places=2, max_digits=6, default=0.00, null=False, blank=False)
    staff_amount = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, default=0.0)
    credit_fee = models.DecimalField(decimal_places=2, max_digits=2, null=False, blank=False, default=.03)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return self.activity.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:activitytip-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:hx-activitytip-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.staff_amount = Decimal(self.tip_amount) * (Decimal(1) - Decimal(self.credit_fee))
        super().save(*args, **kwargs)
 

class ActivityCustomerType(models.TextChoices):
    HOMEKIT = 'h', 'Twist at Home Kit(s) / Pop-In & Paint'

class CustomerStatus(models.TextChoices):
    PENDING = 'p', 'Pending Processing'
    COMPLETED = 'c', 'Completed Processing'

class ActivityCustomer(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=ActivityCustomerType.choices, default=ActivityCustomerType.HOMEKIT)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, default=0.0, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=CASCADE, null=False, blank=False, related_name='activity_customer_product', default=1)
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
        return self.activity.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:activitycustomer-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:hx-activitycustomer-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.total_customer_qty = self.per_customer_qty * self.quantity
        self.subtotal_price = self.quantity * self.price
        self.date = self.activity.date
        if self.type == 'h':
            self.taxes = self.subtotal_price * self.activity.tax_rate
            self.total_price = self.subtotal_price + self.taxes
            self.cost_factor = self.quantity * self.price
            try:
                product_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.activity.date).order_by('-date').first())
                self.product_cost = product_cost[0] * self.total_customer_qty
            except:
                product_cost = Decimal(1.99)
                self.product_cost = product_cost * self.total_customer_qty

        elif self.type == 'p':
            self.taxes = self.subtotal_price * self.activity.tax_rate
            self.total_price = self.subtotal_price + self.taxes
            self.cost_factor = self.quantity * self.price
            try:
                product_cost = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.activity.date).order_by('-date').first())
                self.product_cost = product_cost[0] * self.total_customer_qty
            except:
                product_cost = Decimal(1.99)
                self.product_cost = product_cost * self.total_customer_qty

        elif self.type == 'r':
            try:
                cost_factor = list(PurchaseItem.objects.values_list('price_each').filter(product=self.product, date__lte=self.activity.date).order_by('-date').first())
                self.cost_factor = cost_factor[0] * self.total_customer_qty
                self.product_cost = self.cost_factor
                self.taxes = self.cost_factor * self.activity.tax_rate
            except:
                cost_factor = Decimal(1.99)
                self.cost_factor = cost_factor * self.total_customer_qty
                self.taxes = self.cost_factor * self.activity.tax_rate

            self.total_price = self.subtotal_price
        super().save(*args, **kwargs)
    
def activity_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"activities/{new_fname}{fpath.suffix}"


class ActivityImages(models.Model):
    activity = models.ForeignKey(Activity, on_delete=CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    upload = models.ImageField(upload_to=activity_image_upload_handler, height_field=None, width_field=None, max_length=100)

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:activityimage-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:hx-activityimage-update", kwargs=kwargs)



class ActivityAdminPay(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    admin_pay = models.DecimalField(decimal_places=2, max_digits=5, default=0.00, null=False, blank=False)
    status = models.CharField(max_length=1, choices=PayStatus.choices, default=PayStatus.PENDING)
    note = models.CharField(max_length=50, null=False, blank=False, default='Add Justification Note')
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.activity.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:activityadminpay-delete", kwargs=kwargs)

    def get_htmx_edit_url(self):
        kwargs = {
            "parent_slug": self.activity.slug,
            "id": self.id
        }
        return reverse("activities:hx-activityadminpay-update", kwargs=kwargs)

    def save(self, *args, **kwargs):
        activity_length = Activity.objects.get(id=self.activity.id)
        self.date = activity_length.date
        super().save(*args, **kwargs)
