from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('first_name', 'last_name', 'email', 'username', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superadmin', 'is_admin')
    ordering=('last_login',)
    fieldsets=()
    filter_horizontal=()
    list_filter=()
    
    
admin.site.register(Account, AccountAdmin)