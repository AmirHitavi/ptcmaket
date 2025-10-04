import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestApplyApplicationCreation:
    url = reverse("create-apply-application")

    def test_if_data_valid_returns_201(self, api_client):

        resume_content = b"Fake PDF content for testing"
        resume_file = SimpleUploadedFile(
            "test_resume.pdf", resume_content, content_type="application/pdf"
        )

        valid_data = {
            "first_name": "test first name",
            "last_name": "test  last name",
            "email": "test@email.com",
            "phone_number": "test phone",
            "education_degree": "test education degree",
            "study_field": "test study field",
            "resume": resume_file,
            "cover_letter": "test cover letter",
        }

        response = api_client.post(self.url, valid_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_iv_data_invalid_returns_400(self, api_client):
        invalid_data = {}

        response = api_client.post(self.url, invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_resume_not_pdf_returns_400(self, api_client):
        resume_content = b"Fake txt content for testing"
        resume_file = SimpleUploadedFile(
            "test_resume.txt", resume_content, content_type="text/plain"
        )

        invalid_data = {
            "first_name": "test first name",
            "last_name": "test  last name",
            "email": "test@email.com",
            "phone_number": "test phone",
            "education_degree": "test education degree",
            "study_field": "test study field",
            "resume": resume_file,
            "cover_letter": "test cover letter",
        }

        response = api_client.post(self.url, invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
