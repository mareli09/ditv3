from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status', 'id_number', 'department', 'course')
    search_fields = ('user__username', 'id_number', 'role')
    list_filter = ('role', 'status', 'department')
