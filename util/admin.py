from django.contrib import admin
from .models import logs
# Register your models here.

class LogsAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'user', 'log']

admin.site.register(logs, LogsAdmin)
