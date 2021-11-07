from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.deletion import SET_NULL
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from events.utils import slugify_instance_title

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True, unique=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now, null=True, blank=True)

    objects = ArticleManager()

    @property
    def name(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug" : self.slug})

    def get_hx_url(self):
        return reverse("articles:hx-detail", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("articles:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("articles:delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = [('-publish'), ]


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)
