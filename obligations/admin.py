from django.contrib import admin
from .models import Obligation


@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    list_display = ['title', 'owed_by', 'owed_to', 'status', 'due_at', 'created_at']
    list_filter = ['status', 'created_at', 'due_at']
    search_fields = ['title', 'description', 'owed_by__email', 'owed_to__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'cancelled_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description')
        }),
        ('People', {
            'fields': ('owed_by', 'owed_to')
        }),
        ('Status & Timing', {
            'fields': ('status', 'due_at', 'completed_at', 'cancelled_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
