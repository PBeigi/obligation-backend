from django.db import models
from django.conf import settings
from django.utils import timezone


class Obligation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Relationships
    owed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='obligations_as_ower',
        help_text='Person who owes the obligation'
    )
    owed_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='obligations_as_requester',
        help_text='Person to whom the obligation is owed'
    )
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    due_at = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'obligations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owed_by', 'status', 'due_at']),
            models.Index(fields=['owed_to', 'status', 'due_at']),
            models.Index(fields=['status', 'due_at']),
        ]
    
    def is_overdue(self):
        """Check if obligation is past due date and still pending"""
        return self.status == 'PENDING' and self.due_at < timezone.now()
    
    def __str__(self):
        return f"{self.title} ({self.owed_by.email} owes {self.owed_to.email})"
