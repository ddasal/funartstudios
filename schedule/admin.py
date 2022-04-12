from django.contrib import admin
from schedule.models import ScheduleChange, Typical

# Register your models here.

class TypicalScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated']

admin.site.register(Typical, TypicalScheduleAdmin)

class ChangeScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated']

admin.site.register(ScheduleChange, ChangeScheduleAdmin)
