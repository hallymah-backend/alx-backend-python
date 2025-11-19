from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)