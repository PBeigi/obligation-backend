from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from .models import Obligation
from notifications.models import Notification
from audit.models import AuditEvent


@transaction.atomic()
def complete_obligation(obligation, user):
    """
    Mark an obligation as completed. Only the person who owes (owed_by) can complete.
    
    Idempotent: returns the obligation even if already completed.
    Creates audit event and notification in the same transaction.
    """
    # Explicit permission check
    if user != obligation.owed_by:
        raise PermissionDenied("Only the person who owes can complete this obligation.")
    
    # Idempotent: if already completed, return existing
    if obligation.status == 'COMPLETED':
        return obligation
    
    # Capture old status for audit
    old_status = obligation.status
    
    # Update obligation
    obligation.status = 'COMPLETED'
    obligation.completed_at = timezone.now()
    obligation.save(update_fields=['status', 'completed_at', 'updated_at'])
    
    # Create audit event
    AuditEvent.objects.create(
        obligation=obligation,
        user=user,
        action='COMPLETED',
        metadata={
            'obligation_id': obligation.id,
            'from': old_status,
            'to': 'COMPLETED'
        }
    )
    
    # Create notification for the person who was waiting
    Notification.objects.create(
        user=obligation.owed_to,
        type='COMPLETED',
        obligation=obligation,
        metadata={
            'obligation_id': obligation.id,
            'title': obligation.title
        }
    )
    
    return obligation


@transaction.atomic()
def cancel_obligation(obligation, user):
    """
    Cancel an obligation. Only the person who requested it (owed_to) can cancel.
    
    Idempotent: returns the obligation even if already cancelled.
    Creates audit event and notification in the same transaction.
    """
    # Explicit permission check
    if user != obligation.owed_to:
        raise PermissionDenied("Only the person who requested this obligation can cancel it.")
    
    # Idempotent: if already cancelled, return existing
    if obligation.status == 'CANCELLED':
        return obligation
    
    # Capture old status for audit
    old_status = obligation.status
    
    # Update obligation
    obligation.status = 'CANCELLED'
    obligation.cancelled_at = timezone.now()
    obligation.save(update_fields=['status', 'cancelled_at', 'updated_at'])
    
    # Create audit event
    AuditEvent.objects.create(
        obligation=obligation,
        user=user,
        action='CANCELLED',
        metadata={
            'obligation_id': obligation.id,
            'from': old_status,
            'to': 'CANCELLED'
        }
    )
    
    # Create notification for the person who owed
    Notification.objects.create(
        user=obligation.owed_by,
        type='CANCELLED',
        obligation=obligation,
        metadata={
            'obligation_id': obligation.id,
            'title': obligation.title
        }
    )
    
    return obligation
