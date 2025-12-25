from rest_framework import permissions


class IsOwedByOrOwedTo(permissions.BasePermission):
    """
    Object-level permission to only allow users who are either:
    - owed_by (person who owes the obligation)
    - owed_to (person to whom the obligation is owed)
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owed_by == request.user or obj.owed_to == request.user
