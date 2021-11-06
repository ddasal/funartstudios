from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_home = models.CharField(max_length=10, blank=True) #  change the field to watever works for you
    phone_mobile = models.CharField(max_length=10, blank=True) #  change the field to watever works for you
    address = models.CharField(max_length=220, null=True, blank=True)
    city = models.CharField(max_length=220, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    emergency_contact_name_1 = models.CharField(max_length=220, null=True, blank=True)
    emergency_contact_number_1 = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact_email_1 = models.CharField(max_length=220, null=True, blank=True)
    emergency_contact_name_2 = models.CharField(max_length=220, null=True, blank=True)
    emergency_contact_number_2 = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact_email_2 = models.CharField(max_length=220, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
        

#  This will auto create a profile of user with blank phone number that can be updated later.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class UserPay(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=CASCADE)
    start_date = models.DateField(null=False, blank=False, default=timezone.now)
    end_date = models.DateField(null=False, blank=False, default=timezone.now)
    stage = models.DecimalField(decimal_places=2, max_digits=4, default=0.00, null=False, blank=False)
    floor = models.DecimalField(decimal_places=2, max_digits=4, default=0.00, null=False, blank=False)
    team = models.DecimalField(decimal_places=2, max_digits=4, default=0.00, null=False, blank=False)
    prepaint_single = models.DecimalField(decimal_places=2, max_digits=4, default=13.00, null=False, blank=False)
    prepaint_double = models.DecimalField(decimal_places=2, max_digits=4, default=19.50, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
