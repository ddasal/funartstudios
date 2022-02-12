from django.contrib import admin

from products.models import Product, PurchaseItem, PurchaseOrder

# Register your models here.


admin.site.register(Product)

class PurchaseItemsInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0

class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemsInline]
    list_display = ['id', 'supplier', 'date', 'user']
    readonly_fields = ['timestamp', 'updated']
    ordering = ['-date']

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
