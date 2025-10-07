from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_resume


class Contact(models.Model):
    first_name = models.CharField(verbose_name=_("نام"), max_length=100)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=100)
    phone_number = models.CharField(verbose_name=_("شماره تلفن"), max_length=50)
    message = models.TextField(verbose_name=_("پیام"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("تماس")
        verbose_name_plural = _("تماس‌ها")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contact: {self.first_name} {self.last_name}:{self.email}."


class Order(models.Model):
    company_name = models.CharField(verbose_name=_("نام شرکت"), max_length=100)
    activity_area = models.CharField(verbose_name=_("حوزه فعالیت"), max_length=100)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=100)
    contact_number = models.CharField(verbose_name=_("شماره تماس"), max_length=50)
    explanation = models.TextField(verbose_name=_("توضیحات"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش‌ها")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order from {self.company_name}:{self.email}."


class ApplyApplication(models.Model):
    class ApplyApplicationStatusChoice(models.TextChoices):
        PENDING = "P", _("در انتظار")
        REVIEWED = "RV", _("بررسی شده")
        REJECTED = "RJ", _("رد شده")
        ACCEPTED = "A", _("پذیرفته شده")

    first_name = models.CharField(verbose_name=_("نام"), max_length=100)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=100)
    phone_number = models.CharField(verbose_name=_("شماره تلفن"), max_length=50)
    education_degree = models.CharField(verbose_name=_("میزان تحصیلات"), max_length=100)
    study_field = models.CharField(verbose_name=_("رشته تحصیلی"), max_length=100)
    resume = models.FileField(
        verbose_name=_("فایل رزومه"),
        upload_to="resumes/",
        validators=[validate_resume],
    )
    cover_letter = models.TextField(verbose_name=_("نامه همراه"))
    status = models.CharField(
        verbose_name=_("وضعیت"),
        max_length=2,
        choices=ApplyApplicationStatusChoice.choices,
        default=ApplyApplicationStatusChoice.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("درخواست همکاری")
        verbose_name_plural = _("درخواست‌های همکاری")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Resume from {self.first_name} {self.last_name}."
