from django.contrib import admin
from django.db import models

from events.models import AdminPay, Event, EventCustomer, EventImages, EventStaff, EventTax, EventTip

# Register your models here.

class EventCustomerInline(admin.TabularInline):
    model = EventCustomer
    extra = 0
    readonly_fields = ['cost_factor', 'subtotal_price', 'taxes', 'total_price', 'timestamp', 'updated']

class EventTipInline(admin.TabularInline):
    model = EventTip
    extra = 0
    readonly_fields = ['floor_split', 'stage_amount', 'floor_amount', 'timestamp', 'updated']

class EventImageInline(admin.TabularInline):
    model = EventImages
    extra = 0

class EventStaffInline(admin.TabularInline):
    model = EventStaff
    extra = 0
    readonly_fields = ['rate', 'prepaint_pay', 'hourly_pay', 'total_pay', 'timestamp', 'updated', 'staff_notes']

class AdminPayInline(admin.TabularInline):
    model = AdminPay
    extra = 0
    readonly_fields = ['timestamp', 'updated']

class EventAdmin(admin.ModelAdmin):
    inlines = [EventCustomerInline, EventStaffInline, AdminPayInline, EventTipInline, EventImageInline]
    list_display = ['title', 'date', 'time', 'updated']
    search_fields = ['title']
    readonly_fields = ['tax_rate', 'timestamp', 'updated', 'payroll_report', 'royalty_report']
    ordering = ['-date', '-time']

admin.site.register(Event, EventAdmin)

class EventTaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_rate', 'start_date', 'end_date']
    readonly_fields = ['timestamp', 'updated']
    ordering = ['-start_date']

admin.site.register(EventTax, EventTaxAdmin)