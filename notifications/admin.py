from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'obligation', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['user__email', 'obligation__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'type', 'obligation')
        }),
        ('Details', {
            'fields': ('metadata', 'is_read', 'created_at')
        }),
    )
