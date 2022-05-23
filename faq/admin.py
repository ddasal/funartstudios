from django.contrib import admin

# Register your models here.
from .models import Faq

class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'updated']
    search_fields = ['question', 'answer']

admin.site.register(Faq, FaqAdmin)
