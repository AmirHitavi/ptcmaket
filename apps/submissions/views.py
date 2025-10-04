from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import (ApplyApplicationSerializer, ContactSerializer,
                          OrderSerializer)


class ContactAPIView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


class OrderAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class ApplyApplicationAPIView(CreateAPIView):
    serializer_class = ApplyApplicationSerializer
    permission_classes = [AllowAny]
