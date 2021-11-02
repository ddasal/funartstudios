from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from .utils import slugify_instance_title
from django.db.models.signals import pre_save, post_save

User = settings.AUTH_USER_MODEL


# Create your models here.
"""
Event
 - title
 - date
 - time
 - timestamp
 - updated
 - worker
 - customer


"""
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
    STANDARD = 's', 'Stanrd Event'
    PAINTPOUR = 'p', 'Paint Pour Event'
    TAXFREE = 't', 'Other Tax Free Event'

class EventQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) #| Q(content__icontains=query)
        return self.filter(lookups)

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Event(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False, default=timezone.now, auto_now=False, auto_now_add=False)
    time = models.TimeField(null=False, blank=False, default=timezone.now)
    length = models.CharField(max_length=4, choices=EventLength.choices, default=EventLength.TWOHOUR)
    type = models.CharField(max_length=1, choices=EventType.choices, default=EventType.STANDARD)
    slug = models.SlugField(null=True, blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug" : self.slug})



def event_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(event_pre_save, sender=Event)

def event_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(event_post_save, sender=Event)
