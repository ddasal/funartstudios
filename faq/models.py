from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from events.utils import slugify_instance_title

User = settings.AUTH_USER_MODEL

class FaqQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class FaqManager(models.Manager):
    def get_queryset(self):
        return FaqQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Category(models.TextChoices):
    FAM = 'f', 'FAM'
    FASADMIN = 'a', 'FAS Admin'
    GENERAL = 'g', 'General'
    POPIN = 'p', 'Pop-In & Paint'
    PRIVATE = 'r', 'Private Parties'
    PWAP = 'w', 'Painting with a Purpose'
    SQUAREUP = 's', 'Square'
    TWISTATHOME = 't', 'Twist at Home Kits'

class Faq(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=1, choices=Category.choices, default=Category.GENERAL)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    page_views = models.IntegerField(default=0, null=False, blank=False)

    objects = FaqManager()

    @property
    def name(self):
        return self.question

    @property
    def title(self):
        return self.question
        
    def get_absolute_url(self):
        return reverse("faq:detail", kwargs={"id" : self.id})

    def get_hx_url(self):
        return reverse("faq:hx-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("faq:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("faq:delete", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = [('category'), ]

