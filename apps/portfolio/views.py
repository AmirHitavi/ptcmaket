from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Blog, Comment, GalleryItem, Project
from .paginations import DefaultPageNumberPagination
from .serializers import (
    BlogDetailsSerializer,
    BlogListSerializer,
    CommentSerializer,
    ProjectDetailsSerializer,
    ProjectListSerializer,
    ReplySerializer,
)


@extend_schema(
    tags=["Projects"],
    summary="Get List of all projects",
    description="Retrieve a paginated list of projects with advanced filtering and search capabilities.",
)
class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {"category__title": ["iexact"], "status": ["iexact"]}
    search_fields = {"title": ["icontains"], "category__title": ["icontains"]}
    pagination_class = DefaultPageNumberPagination

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


@extend_schema(
    tags=["Projects"],
    summary="Get Details of a project.",
    description="Retrieve a project with its details.",
)
class ProjectDetailsAPIView(RetrieveAPIView):
    serializer_class = ProjectDetailsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.all()


@extend_schema(
    tags=["Blogs"],
    summary="Get List of all blogs",
    description="Retrieve a paginated list of blogs.",
)
class BlogListAPIView(ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    queryset = Blog.objects.filter(status=Blog.BlogStatus.PUBLISHED)
    pagination_class = DefaultPageNumberPagination


@extend_schema(
    tags=["Blogs"],
    summary="Get Details of a blog",
    description="Retrieve a blog with its details.",
)
class BlogDetailsAPIView(RetrieveAPIView):
    serializer_class = BlogDetailsSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Blog.objects.prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.filter(
                    status=Comment.CommentStatusChoice.APPROVED
                ).select_related("parent"),
                to_attr="all_approved_comments",
            )
        )


@extend_schema(
    tags=["Blogs", "Comments"],
    summary="Create a new comment for a given blog",
    description="Create a new comment for a given blog and returns response 201",
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


@extend_schema(
    tags=["Blogs", "Comments"],
    summary="Create a reply  for a given comment",
    description="Create a new comment for a given comment and returns response 201",
)
class ReplyCreateAPIView(CreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

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
            raise ValidationError(_("Parent comment does not belong to this blog"))

        serializer.save(blog=blog, parent=parent)
