from rest_framework import serializers

from .models import ApplyApplication, Contact, Order


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "phone_number", "message"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "company_name",
            "activity_area",
            "email",
            "contact_number",
            "explanation",
        ]


class ApplyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyApplication
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "education_degree",
            "study_field",
            "resume",
            "cover_letter",
        ]
