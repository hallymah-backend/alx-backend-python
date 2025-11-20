from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    Used to ensure users can only view their own messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission ensuring:
    1. Only authenticated users can access the API
    2. Only participants of the conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # 1) Must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is a Message or Conversation

        conversation = getattr(obj, "conversation", obj)

        # Check if the user is a participant
        if request.user not in conversation.participants.all():
            return False

        # Allow all safe methods (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow message creation (POST)
        if request.method == "POST":
            return True

        # Allow update and delete for participants
        if request.method in ("PUT", "PATCH", "DELETE"):
            return True

        return False
