from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from rest_framework.response import Response


class UserMessagesView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Only show messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Auto-set sender as the logged-in user
        serializer.save(sender=self.request.user)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
class ConversationMessagesView(generics.ListCreateAPIView):
    # """
    # GET: List all messages in a conversation
    # POST: Send message in conversation
    # """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Allow only participants
        if self.request.user not in conversation.participants.all():
            from rest_framework.status import HTTP_403_FORBIDDEN
            return Response({"detail": "Forbidden"}, status=HTTP_403_FORBIDDEN)

        return conversation.messages.all()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Ensure authenticated user is a participant
        if self.request.user not in conversation.participants.all():
            from rest_framework.status import HTTP_403_FORBIDDEN
            raise PermissionDenied("Forbidden", code=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
