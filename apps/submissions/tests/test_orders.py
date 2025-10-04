import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestOrderCreation:

    url = reverse("create-order")

    @pytest.mark.django_db
    def test_if_data_valid_returns_201(self, api_client):
        valid_data = {
            "company_name": "company",
            "activity_area": "it",
            "email": "company@gmail.com",
            "contact_number": "0993990",
            "explanation": "company explanation",
        }

        response = api_client.post(self.url, valid_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_invalid_returns_400(self, api_client):
        invalid_data = {}

        response = api_client.post(self.url, invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
