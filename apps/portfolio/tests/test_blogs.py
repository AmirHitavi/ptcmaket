import pytest
from django.urls import reverse
from rest_framework import status

from .factories import BlogFactory


@pytest.mark.django_db
class TestBlogs:

    def test_get_list_of_blogs_and_returns_200(self, api_client):
        blogs = BlogFactory.create_batch(5)

        response = api_client.get(reverse("list-blogs"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 5

    def test_get_details_blog_and_return_200(self, api_client):
        blog = BlogFactory.create(comments=5)

        response = api_client.get(reverse("details-blogs", args=[blog.slug]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("title") == blog.title
        assert len(response.data.get("comments")) == 5
