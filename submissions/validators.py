from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def validate_resume(file):
    file_extension = file.name.split(".")[-1]

    if file_extension != "pdf":
        raise ValidationError(_("Only Pdf files are allowed."))
