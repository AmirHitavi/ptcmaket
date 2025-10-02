from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ApplyApplication, Contact, Order


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone_number", "created_at"]
    list_per_page = 20
    search_fields = ["first_name", "lsat_name", "email", "phone_number"]
    search_help_text = _(
        "Search for contact via fist name, last name, email, phone number"
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["company_name", "activity_area", "email", "contact_number"]
    list_per_page = 20
    search_fields = ["company_name", "activity_area", "email", "contact_number"]
    search_help_text = _(
        "Search for contact via company name, activity area, email, phone number"
    )


@admin.register(ApplyApplication)
class ApplyApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "education_degree",
        "status",
        "created_at",
    ]
    list_per_page = 20
    list_filter = ["status"]
    list_editable = ["status"]
    search_fields = ["first_name, last_name", "email", "phone_number"]
    search_help_text = _("Search via first name, last name, email, phone number")
