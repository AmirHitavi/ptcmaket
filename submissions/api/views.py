from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .serializers import ApplyApplicationSerializer, ContactSerializer, OrderSerializer


@extend_schema(
    tags=["Submissions"],
    summary="Create a contact",
)
class ContactViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Submissions"],
    summary="Create an Order",
)
class OrderViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Submissions"],
    summary="Create an apply application",
)
class ApplyApplicationViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ApplyApplicationSerializer
    permission_classes = [AllowAny]
