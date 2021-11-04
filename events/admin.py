from django.contrib import admin
from django.db import models

from events.models import Event, EventCustomer, EventStaff

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'updated']
    search_fields = ['title']
    readonly_fields = ['timestamp', 'updated']
    ordering = ['-date', '-time']

admin.site.register(Event, EventAdmin)

admin.site.register(EventStaff)

admin.site.register(EventCustomer)