from django.db import models
from django.conf import settings
from django.utils import timezone


class AuditEvent(models.Model):
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('OVERDUE', 'Marked Overdue'),
        ('UPDATED', 'Updated'),
    ]
    
    obligation = models.ForeignKey(
        'obligations.Obligation',
        on_delete=models.CASCADE,
        related_name='audit_events'
    )
    
    # Who performed the action (null for system actions)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='User who performed action, null for system'
    )
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional context about what changed
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['obligation', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        actor = self.user.email if self.user else 'System'
        return f"{self.get_action_display()} by {actor} on {self.obligation.title}"
