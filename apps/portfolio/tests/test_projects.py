import pytest
from django.urls import reverse
from rest_framework import status

from .factories import ProjectFactory


@pytest.mark.django_db
class TestProjects:
    def test_get_list_projects_and_returns_200(self, api_client):
        ProjectFactory.create_batch(5)

        response = api_client.get(reverse("list-projects"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 5

    def test_get_details_project_and_return_200(self, api_client):
        project = ProjectFactory.create(gallery_items=3)

        response = api_client.get(reverse("details-projects", args=[project.slug]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("title") == project.title
        assert len(response.data.get("gallery_items")) == 3
