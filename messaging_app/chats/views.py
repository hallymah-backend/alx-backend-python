from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsOwner

class UserMessagesView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)
