import pytest
from django.urls import reverse
from rest_framework import status

from .factories import HistoryFactory


@pytest.mark.django_db
class TestHistories:
    def test_get_list_histories_and_returns_200(self, api_client):
        HistoryFactory.create_batch(5)

        response = api_client.get(reverse("history-list"))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
