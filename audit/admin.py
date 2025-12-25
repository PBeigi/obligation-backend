from django.contrib import admin
from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ['obligation', 'action', 'user', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['obligation__title', 'user__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['obligation', 'user', 'action', 'created_at', 'metadata']
    
    def has_add_permission(self, request):
        # Audit events should only be created by the system
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of audit trail
        return False
