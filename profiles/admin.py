from django.contrib import admin
from .models import User, Role


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('roles',)  # This is for Many-to-Many relationship


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
