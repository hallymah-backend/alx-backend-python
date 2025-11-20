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
    Only allow participants of a conversation to:
    - view messages
    - send messages
    - update messages
    - delete messages
    """
    def has_object_permission(self, request, view, obj):
        """
        obj will be a Message or Conversation instance.
        We assume each obj has a conversation with participants.
        """
        user = request.user

        # conversation.participants is a ManyToManyField(User)
        return user in obj.conversation.participants.all()