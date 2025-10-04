from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_resume


class Contact(models.Model):
    first_name = models.CharField(verbose_name=_("Contact First Name"), max_length=100)
    last_name = models.CharField(verbose_name=_("Contact Last Name"), max_length=100)
    email = models.EmailField(verbose_name=_("Contact Email"), max_length=100)
    phone_number = models.CharField(
        verbose_name=_("Contact Phone Number"), max_length=50
    )
    message = models.TextField(verbose_name=_("Contact Message"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contact: {self.first_name} {self.last_name}:{self.email}."


class Order(models.Model):
    company_name = models.CharField(
        verbose_name=_("Order Company Name"), max_length=100
    )
    activity_area = models.CharField(
        verbose_name=_("Order Activity Area"), max_length=100
    )
    email = models.EmailField(verbose_name=_("Order Email"), max_length=100)
    contact_number = models.CharField(
        verbose_name=_("Order Contact Number"), max_length=50
    )
    explanation = models.TextField(verbose_name=_("Order Explanation"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order from {self.company_name}:{self.email}."


class ApplyApplication(models.Model):
    class ApplyApplicationStatusChoice(models.TextChoices):
        PENDING = "P", _("Pending")
        REVIEWED = "RV", _("Reviewed")
        REJECTED = "RJ", _("Rejected")
        ACCEPTED = "A", _("Accepted")

    first_name = models.CharField(verbose_name=_("Apply First Name"), max_length=100)
    last_name = models.CharField(verbose_name=_("Apply Last Name"), max_length=100)
    email = models.EmailField(verbose_name=_("Apply Email"), max_length=100)
    phone_number = models.CharField(verbose_name=_("Apply Phone Number"), max_length=50)
    education_degree = models.CharField(
        verbose_name=_("Apply Education Degree"), max_length=100
    )
    study_field = models.CharField(verbose_name=_("Apply Study Field"), max_length=100)
    resume = models.FileField(
        verbose_name=_("Apply Resume File"),
        upload_to="resumes/",
        validators=[validate_resume],
    )
    cover_letter = models.TextField(verbose_name=_("Apply Cover Letter"))
    status = models.CharField(
        verbose_name=_("Apply Status"),
        max_length=2,
        choices=ApplyApplicationStatusChoice.choices,
        default=ApplyApplicationStatusChoice.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Apply Application")
        verbose_name_plural = _("Apply Applications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Resume from {self.first_name} {self.last_name}."
