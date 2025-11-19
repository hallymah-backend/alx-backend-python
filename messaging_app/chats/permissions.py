from rest_framework import BasePermission, permissions
class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    Used to ensure users can only view their own messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
