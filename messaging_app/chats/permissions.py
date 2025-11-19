from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    Used to ensure users can only view their own messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
