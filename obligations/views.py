from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Obligation
from .serializers import ObligationSerializer, ObligationCreateSerializer
from .permissions import IsOwedByOrOwedTo
from .services import complete_obligation, cancel_obligation
from audit.models import AuditEvent
from audit.serializers import AuditEventSerializer


class ObligationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Obligation CRUD and actions.
    
    List filtering:
    - ?role=owed_by - obligations you owe
    - ?role=owed_to - obligations owed to you
    - ?status=PENDING|COMPLETED|OVERDUE|CANCELLED
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Optimize queries with select_related and apply filters"""
        queryset = Obligation.objects.select_related('owed_by', 'owed_to')
        
        # Filter by role
        role = self.request.query_params.get('role')
        if role == 'owed_by':
            queryset = queryset.filter(owed_by=self.request.user)
        elif role == 'owed_to':
            queryset = queryset.filter(owed_to=self.request.user)
        else:
            # Default: show obligations where user is involved
            queryset = queryset.filter(
                owed_by=self.request.user
            ) | queryset.filter(
                owed_to=self.request.user
            )
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        valid_statuses = dict(Obligation.STATUS_CHOICES).keys()
        if status_param and status_param in valid_statuses:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    
    def get_permissions(self):
        """Apply object-level permissions for detail actions"""
        if self.action in ['retrieve', 'complete', 'cancel', 'audit_events']:
            return [IsAuthenticated(), IsOwedByOrOwedTo()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Use different serializers for input vs output"""
        if self.action == 'create':
            return ObligationCreateSerializer
        return ObligationSerializer
    
    def perform_create(self, serializer):
        """Set owed_to to current user"""
        serializer.save(owed_to=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark obligation as completed (owed_by only)"""
        obligation = self.get_object()
        updated_obligation = complete_obligation(obligation, request.user)
        serializer = ObligationSerializer(updated_obligation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel obligation (owed_to only)"""
        obligation = self.get_object()
        updated_obligation = cancel_obligation(obligation, request.user)
        serializer = ObligationSerializer(updated_obligation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def audit_events(self, request, pk=None):
        """Get audit trail for this obligation"""
        obligation = self.get_object()
        events = AuditEvent.objects.filter(
            obligation=obligation
        ).select_related('user').order_by('-created_at')
        serializer = AuditEventSerializer(events, many=True)
        return Response(serializer.data)
