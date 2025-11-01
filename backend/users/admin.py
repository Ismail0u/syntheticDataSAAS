from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom administration configuration for the extended User model.
    
    This configuration customizes the Django admin interface to display, filter, 
    and edit the SAAS-specific fields (plan, quota, role).
    """ 
    list_display = ['email', 'username', 'plan', 'role', 'daily_quota_used', 'is_active', 'date_joined']
    
    list_filter = ['plan', 'role', 'is_active', 'is_staff', 'date_joined']
    
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    # Custom grouping of fields on the user detail page for better organization
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('username', 'email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name')
        }),
        ('Plan et Permissions', {
            'fields': ('plan', 'role', 'daily_quota_used', 'last_quota_reset')
        }),
        ('Statut', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fields that cannot be edited via the admin interface
    readonly_fields = ['last_login', 'date_joined']