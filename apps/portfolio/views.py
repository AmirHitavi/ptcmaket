from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Blog, Comment, GalleryItem, Project
from .serializers import (
    BlogDetailsSerializer,
    BlogListSerializer,
    CommentSerializer,
    ProjectDetailsSerializer,
    ProjectListSerializer,
    ReplySerializer,
)


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Project.objects.select_related("category")
            .prefetch_related(
                Prefetch(
                    "gallery_items", queryset=GalleryItem.objects.order_by("created_at")
                )
            )
            .order_by("-created_at", "title")
        )


class ProjectDetailsAPIView(RetrieveAPIView):
    serializer_class = ProjectDetailsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.all()


class BlogListAPIView(ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    queryset = Blog.objects.filter(status=Blog.BlogStatus.PUBLISHED)


class BlogDetailsAPIView(RetrieveAPIView):
    serializer_class = BlogDetailsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    # TODO: N+1 Problem query
    def get_queryset(self):
        approved_comments = Comment.objects.filter(
            status=Comment.CommentStatusChoice.APPROVED
        ).select_related("parent")
        return Blog.objects.prefetch_related(
            Prefetch("comments", queryset=approved_comments)
        )


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_blog(self):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        return blog

    def perform_create(self, serializer):
        blog = self.get_blog()
        serializer.save(blog=blog)


class ReplyCreateAPIView(CreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]

    def get_blog(self):
        blog_slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=blog_slug)
        return blog

    def get_parent(self):
        parent_pk = self.kwargs.get("pk")
        parent = get_object_or_404(Comment, pk=parent_pk)
        return parent

    def perform_create(self, serializer):
        blog = self.get_blog()
        parent = self.get_parent()

        if parent.blog.id != blog.id:
            return Response(
                {"error": "Parent comment does not belong to this blog"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(blog=blog, parent=parent)
