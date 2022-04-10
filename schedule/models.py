from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class RecurrenceOptions(models.TextChoices):
    WEEKLY = 'w', 'Weekly'
    BIWEEKLY = 'b', 'Bi-Weekly'
    MONTHLY = 'm', 'Once a Month'
    ASKME = 'a', 'Maybe, Ask Me'
    
class Typical(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    monday_8am = models.BooleanField(default=True)
    monday_9am = models.BooleanField(default=True)
    monday_10am = models.BooleanField(default=True)
    monday_11am = models.BooleanField(default=True)
    monday_12pm = models.BooleanField(default=True)
    monday_1pm = models.BooleanField(default=True)
    monday_2pm = models.BooleanField(default=True)
    monday_3pm = models.BooleanField(default=True)
    monday_4pm = models.BooleanField(default=True)
    monday_5pm = models.BooleanField(default=True)
    monday_6pm = models.BooleanField(default=True)
    monday_7pm = models.BooleanField(default=True)
    monday_8pm = models.BooleanField(default=True)
    monday_9pm = models.BooleanField(default=True)
    monday_10pm = models.BooleanField(default=True)
    monday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    monday = models.IntegerField(default=0, null=False, blank=False)
    tuesday_8am = models.BooleanField(default=True)
    tuesday_9am = models.BooleanField(default=True)
    tuesday_10am = models.BooleanField(default=True)
    tuesday_11am = models.BooleanField(default=True)
    tuesday_12pm = models.BooleanField(default=True)
    tuesday_1pm = models.BooleanField(default=True)
    tuesday_2pm = models.BooleanField(default=True)
    tuesday_3pm = models.BooleanField(default=True)
    tuesday_4pm = models.BooleanField(default=True)
    tuesday_5pm = models.BooleanField(default=True)
    tuesday_6pm = models.BooleanField(default=True)
    tuesday_7pm = models.BooleanField(default=True)
    tuesday_8pm = models.BooleanField(default=True)
    tuesday_9pm = models.BooleanField(default=True)
    tuesday_10pm = models.BooleanField(default=True)
    tuesday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    tuesday = models.IntegerField(default=0, null=False, blank=False)
    wednesday_8am = models.BooleanField(default=True)
    wednesday_9am = models.BooleanField(default=True)
    wednesday_10am = models.BooleanField(default=True)
    wednesday_11am = models.BooleanField(default=True)
    wednesday_12pm = models.BooleanField(default=True)
    wednesday_1pm = models.BooleanField(default=True)
    wednesday_2pm = models.BooleanField(default=True)
    wednesday_3pm = models.BooleanField(default=True)
    wednesday_4pm = models.BooleanField(default=True)
    wednesday_5pm = models.BooleanField(default=True)
    wednesday_6pm = models.BooleanField(default=True)
    wednesday_7pm = models.BooleanField(default=True)
    wednesday_8pm = models.BooleanField(default=True)
    wednesday_9pm = models.BooleanField(default=True)
    wednesday_10pm = models.BooleanField(default=True)    
    wednesday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    wednesday = models.IntegerField(default=0, null=False, blank=False)
    thursday_8am = models.BooleanField(default=True)
    thursday_9am = models.BooleanField(default=True)
    thursday_10am = models.BooleanField(default=True)
    thursday_11am = models.BooleanField(default=True)
    thursday_12pm = models.BooleanField(default=True)
    thursday_1pm = models.BooleanField(default=True)
    thursday_2pm = models.BooleanField(default=True)
    thursday_3pm = models.BooleanField(default=True)
    thursday_4pm = models.BooleanField(default=True)
    thursday_5pm = models.BooleanField(default=True)
    thursday_6pm = models.BooleanField(default=True)
    thursday_7pm = models.BooleanField(default=True)
    thursday_8pm = models.BooleanField(default=True)
    thursday_9pm = models.BooleanField(default=True)
    thursday_10pm = models.BooleanField(default=True)    
    thursday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    thursday = models.IntegerField(default=0, null=False, blank=False)
    friday_8am = models.BooleanField(default=True)
    friday_9am = models.BooleanField(default=True)
    friday_10am = models.BooleanField(default=True)
    friday_11am = models.BooleanField(default=True)
    friday_12pm = models.BooleanField(default=True)
    friday_1pm = models.BooleanField(default=True)
    friday_2pm = models.BooleanField(default=True)
    friday_3pm = models.BooleanField(default=True)
    friday_4pm = models.BooleanField(default=True)
    friday_5pm = models.BooleanField(default=True)
    friday_6pm = models.BooleanField(default=True)
    friday_7pm = models.BooleanField(default=True)
    friday_8pm = models.BooleanField(default=True)
    friday_9pm = models.BooleanField(default=True)
    friday_10pm = models.BooleanField(default=True)    
    friday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    friday = models.IntegerField(default=0, null=False, blank=False)    
    saturday_8am = models.BooleanField(default=True)
    saturday_9am = models.BooleanField(default=True)
    saturday_10am = models.BooleanField(default=True)
    saturday_11am = models.BooleanField(default=True)
    saturday_12pm = models.BooleanField(default=True)
    saturday_1pm = models.BooleanField(default=True)
    saturday_2pm = models.BooleanField(default=True)
    saturday_3pm = models.BooleanField(default=True)
    saturday_4pm = models.BooleanField(default=True)
    saturday_5pm = models.BooleanField(default=True)
    saturday_6pm = models.BooleanField(default=True)
    saturday_7pm = models.BooleanField(default=True)
    saturday_8pm = models.BooleanField(default=True)
    saturday_9pm = models.BooleanField(default=True)
    saturday_10pm = models.BooleanField(default=True)    
    saturday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    saturday = models.IntegerField(default=0, null=False, blank=False)
    sunday_8am = models.BooleanField(default=True)
    sunday_9am = models.BooleanField(default=True)
    sunday_10am = models.BooleanField(default=True)
    sunday_11am = models.BooleanField(default=True)
    sunday_12pm = models.BooleanField(default=True)
    sunday_1pm = models.BooleanField(default=True)
    sunday_2pm = models.BooleanField(default=True)
    sunday_3pm = models.BooleanField(default=True)
    sunday_4pm = models.BooleanField(default=True)
    sunday_5pm = models.BooleanField(default=True)
    sunday_6pm = models.BooleanField(default=True)
    sunday_7pm = models.BooleanField(default=True)
    sunday_8pm = models.BooleanField(default=True)
    sunday_9pm = models.BooleanField(default=True)
    sunday_10pm = models.BooleanField(default=True)    
    sunday_recurrence =  models.CharField(max_length=1, choices=RecurrenceOptions.choices, default=RecurrenceOptions.WEEKLY)
    sunday = models.IntegerField(default=0, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='schedule_created_by')
    updated_by = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='schedule_updated_by')
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True, default='I prefer to work X events per week.  I may be able to cover some last minute private parties or emergency coverages. Just ask.')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        self.monday = 0
        if self.monday_8am:
            self.monday += 1
        if self.monday_9am:
            self.monday += 1
        if self.monday_10am:
            self.monday += 1
        if self.monday_11am:
            self.monday += 1
        if self.monday_12pm:
            self.monday += 1
        if self.monday_1pm:
            self.monday += 1
        if self.monday_2pm:
            self.monday += 1
        if self.monday_3pm:
            self.monday += 1
        if self.monday_4pm:
            self.monday += 1
        if self.monday_5pm:
            self.monday += 1
        if self.monday_6pm:
            self.monday += 1
        if self.monday_7pm:
            self.monday += 1
        if self.monday_8pm:
            self.monday += 1
        if self.monday_9pm:
            self.monday += 1
        if self.monday_10pm:
            self.monday += 1

        self.tuesday = 0
        if self.tuesday_8am:
            self.tuesday += 1
        if self.tuesday_9am:
            self.tuesday += 1
        if self.tuesday_10am:
            self.tuesday += 1
        if self.tuesday_11am:
            self.tuesday += 1
        if self.tuesday_12pm:
            self.tuesday += 1
        if self.tuesday_1pm:
            self.tuesday += 1
        if self.tuesday_2pm:
            self.tuesday += 1
        if self.tuesday_3pm:
            self.tuesday += 1
        if self.tuesday_4pm:
            self.tuesday += 1
        if self.tuesday_5pm:
            self.tuesday += 1
        if self.tuesday_6pm:
            self.tuesday += 1
        if self.tuesday_7pm:
            self.tuesday += 1
        if self.tuesday_8pm:
            self.tuesday += 1
        if self.tuesday_9pm:
            self.tuesday += 1
        if self.tuesday_10pm:
            self.tuesday += 1

        self.wednesday = 0
        if self.wednesday_8am:
            self.wednesday += 1
        if self.wednesday_9am:
            self.wednesday += 1
        if self.wednesday_10am:
            self.wednesday += 1
        if self.wednesday_11am:
            self.wednesday += 1
        if self.wednesday_12pm:
            self.wednesday += 1
        if self.wednesday_1pm:
            self.wednesday += 1
        if self.wednesday_2pm:
            self.wednesday += 1
        if self.wednesday_3pm:
            self.wednesday += 1
        if self.wednesday_4pm:
            self.wednesday += 1
        if self.wednesday_5pm:
            self.wednesday += 1
        if self.wednesday_6pm:
            self.wednesday += 1
        if self.wednesday_7pm:
            self.wednesday += 1
        if self.wednesday_8pm:
            self.wednesday += 1
        if self.wednesday_9pm:
            self.wednesday += 1
        if self.wednesday_10pm:
            self.wednesday += 1

        self.thursday = 0
        if self.thursday_8am:
            self.thursday += 1
        if self.thursday_9am:
            self.thursday += 1
        if self.thursday_10am:
            self.thursday += 1
        if self.thursday_11am:
            self.thursday += 1
        if self.thursday_12pm:
            self.thursday += 1
        if self.thursday_1pm:
            self.thursday += 1
        if self.thursday_2pm:
            self.thursday += 1
        if self.thursday_3pm:
            self.thursday += 1
        if self.thursday_4pm:
            self.thursday += 1
        if self.thursday_5pm:
            self.thursday += 1
        if self.thursday_6pm:
            self.thursday += 1
        if self.thursday_7pm:
            self.thursday += 1
        if self.thursday_8pm:
            self.thursday += 1
        if self.thursday_9pm:
            self.thursday += 1
        if self.thursday_10pm:
            self.thursday += 1

        self.friday = 0
        if self.friday_8am:
            self.friday += 1
        if self.friday_9am:
            self.friday += 1
        if self.friday_10am:
            self.friday += 1
        if self.friday_11am:
            self.friday += 1
        if self.friday_12pm:
            self.friday += 1
        if self.friday_1pm:
            self.friday += 1
        if self.friday_2pm:
            self.friday += 1
        if self.friday_3pm:
            self.friday += 1
        if self.friday_4pm:
            self.friday += 1
        if self.friday_5pm:
            self.friday += 1
        if self.friday_6pm:
            self.friday += 1
        if self.friday_7pm:
            self.friday += 1
        if self.friday_8pm:
            self.friday += 1
        if self.friday_9pm:
            self.friday += 1
        if self.friday_10pm:
            self.friday += 1

        self.saturday = 0
        if self.saturday_8am:
            self.saturday += 1
        if self.saturday_9am:
            self.saturday += 1
        if self.saturday_10am:
            self.saturday += 1
        if self.saturday_11am:
            self.saturday += 1
        if self.saturday_12pm:
            self.saturday += 1
        if self.saturday_1pm:
            self.saturday += 1
        if self.saturday_2pm:
            self.saturday += 1
        if self.saturday_3pm:
            self.saturday += 1
        if self.saturday_4pm:
            self.saturday += 1
        if self.saturday_5pm:
            self.saturday += 1
        if self.saturday_6pm:
            self.saturday += 1
        if self.saturday_7pm:
            self.saturday += 1
        if self.saturday_8pm:
            self.saturday += 1
        if self.saturday_9pm:
            self.saturday += 1
        if self.saturday_10pm:
            self.saturday += 1

        self.sunday = 0
        if self.sunday_8am:
            self.sunday += 1
        if self.sunday_9am:
            self.sunday += 1
        if self.sunday_10am:
            self.sunday += 1
        if self.sunday_11am:
            self.sunday += 1
        if self.sunday_12pm:
            self.sunday += 1
        if self.sunday_1pm:
            self.sunday += 1
        if self.sunday_2pm:
            self.sunday += 1
        if self.sunday_3pm:
            self.sunday += 1
        if self.sunday_4pm:
            self.sunday += 1
        if self.sunday_5pm:
            self.sunday += 1
        if self.sunday_6pm:
            self.sunday += 1
        if self.sunday_7pm:
            self.sunday += 1
        if self.sunday_8pm:
            self.sunday += 1
        if self.sunday_9pm:
            self.sunday += 1
        if self.sunday_10pm:
            self.sunday += 1

        super().save(*args, **kwargs)

