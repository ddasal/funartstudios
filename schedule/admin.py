from django.contrib import admin
from schedule.models import ScheduleChange, Typical, TimeOffRequest

# Register your models here.

class TypicalScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated']

admin.site.register(Typical, TypicalScheduleAdmin)

class ChangeScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated']

admin.site.register(ScheduleChange, ChangeScheduleAdmin)


class TimeOffRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', 'updated']

admin.site.register(TimeOffRequest, TimeOffRequestAdmin)
