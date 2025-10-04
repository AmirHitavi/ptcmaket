from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import ApplyApplicationSerializer, ContactSerializer, OrderSerializer


@extend_schema(
    tags=["Submissions"],
    summary="Create a contact",
)
class ContactAPIView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Submissions"],
    summary="Create an Order",
)
class OrderAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Submissions"],
    summary="Create an apply application",
)
class ApplyApplicationAPIView(CreateAPIView):
    serializer_class = ApplyApplicationSerializer
    permission_classes = [AllowAny]
