from django.conf import settings
from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class ReportStatus(models.TextChoices):
    PENDING = 'p', 'Pending'
    ABANDONDED = 'a', 'Abandoned'
    COMPLETED = 'c', 'Completed'


class Report(models.Model):
    start_date = models.DateField(null=False, blank=False, default=timezone.now)
    end_date = models.DateField(null=False, blank=False, default=timezone.now)
    pay_date = models.DateField(null=False, blank=False, default=timezone.now)
    payroll_gross = models.DecimalField(max_digits=7, decimal_places=2, default=0, null=False, blank=False)
    status = models.CharField(max_length=1, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    prev_status = models.CharField(max_length=1, null=True, choices=ReportStatus.choices, default=None)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("payroll:detail", kwargs={"id" : self.id})

    def get_hx_url(self):
        return reverse("payroll:hx-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("payroll:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("payroll:delete", kwargs={"id": self.id})

    def get_eventstaff_children(self):
        return self.event_set.all()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
