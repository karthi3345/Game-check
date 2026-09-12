from django.contrib import admin
from .models import User, EnvironmentConfiguration

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')

@admin.register(EnvironmentConfiguration)
class EnvironmentConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'is_active')
