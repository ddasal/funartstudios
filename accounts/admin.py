from django.contrib import admin

from accounts.models import UserProfile, UserPay, FileUpload, FileCategory

# Register your models here.



class UserPayInline(admin.TabularInline):
    model = UserPay
    extra = 0
    readonly_fields = ['timestamp', 'updated']

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserPayInline]
    list_display = ['user', 'phone_mobile', 'start_date', 'active', 'updated']
    readonly_fields = ['timestamp', 'updated']
    ordering = ['user']

admin.site.register(UserProfile, UserProfileAdmin)

class FileUploadInline(admin.TabularInline):
    model = FileUpload
    extra = 0
    readonly_fields = ['timestamp', 'updated']

class FileCategoryAdmin(admin.ModelAdmin):
    inlines = [FileUploadInline]
    list_display = ['title']

admin.site.register(FileCategory, FileCategoryAdmin)
