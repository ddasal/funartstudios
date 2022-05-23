from django.db import models
from django.db.models.deletion import SET_NULL
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class logs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='log_created_by')
    log = models.TextField()

