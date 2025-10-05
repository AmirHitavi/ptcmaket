import pytest
from django.urls import reverse
from rest_framework import status

from .factories import BlogFactory, CommentFactory


@pytest.mark.django_db
class TestCommentCreation:
    def test_if_data_valid_returns_201(self, api_client):
        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }
        blog = BlogFactory.create(comments=0)

        url = reverse("create-comment", args=[blog.slug])
        response = api_client.post(url, valid_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("parent") == None
        assert response.data.get("name") == valid_data.get("name")
        assert blog.comments.count() == 1

    def test_if_data_invalid_returns_400(self, api_client):
        invalid_data = {}
        blog = BlogFactory.create(comments=0)

        url = reverse("create-comment", args=[blog.slug])
        response = api_client.post(url, invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert blog.comments.count() == 0

    def test_if_blog_not_exists_returns_404(self, api_client):
        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }
        blog_slug = "test-slug"

        url = reverse("create-comment", args=[blog_slug])
        response = api_client.post(url, valid_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestReplyCreation:
    def test_if_data_valid_returns_201(self, api_client):
        blog = BlogFactory.create(comments=1)
        comment = blog.comments.first()

        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }

        url = reverse("create-reply", args=[blog.slug, comment.id])
        response = api_client.post(url, valid_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert blog.comments.count() == 2
        assert comment.replies.count() == 1

    def test_if_data_invalid_returns_400(self, api_client):
        blog = BlogFactory.create(comments=1)
        comment = blog.comments.first()

        invalid_data = {}

        url = reverse("create-reply", args=[blog.slug, comment.id])
        response = api_client.post(url, invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert blog.comments.count() == 1
        assert comment.replies.count() == 0

    def test_if_comment_not_exist_returns_404(self, api_client):
        blog = BlogFactory.create(comments=0)
        comment_id = 1

        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }

        url = reverse("create-reply", args=[blog.slug, comment_id])
        response = api_client.post(url, valid_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_blog_not_exist_returns_404(self, api_client):
        blog = BlogFactory.create(comments=1)
        comment = CommentFactory.create()
        blog_slug = blog.slug
        blog.delete()

        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }

        url = reverse("create-reply", args=[blog_slug, comment.id])
        response = api_client.post(url, valid_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_blog_not_parent_blog_returns_400(self, api_client):
        blog1 = BlogFactory.create(comments=0)
        blog2 = BlogFactory.create(comments=1)
        first_comment_blog2 = blog2.comments.first()

        valid_data = {
            "name": "test name",
            "email": "test@email.com",
            "text": "test text",
        }

        url = reverse("create-reply", args=[blog1.slug, first_comment_blog2.id])
        response = api_client.post(url, valid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Parent comment does not belong to this blog" in str(response.data)
