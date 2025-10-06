from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from ..models import Blog, Comment, GalleryItem, Project
from .paginations import DefaultPageNumberPagination
from .serializers import BlogSerializer, CommentSerializer, ProjectSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Projects"],
        summary="Get List of all projects",
        description="Retrieve a paginated list of projects with advanced filtering and search capabilities.",
    ),
    retrieve=extend_schema(
        tags=["Projects"],
        summary="Get Details of a project",
        description="Retrieve a project with its details.",
    ),
)
class ProjectViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {"category__title": ["iexact"], "status": ["iexact"]}
    search_fields = {"title": ["icontains"], "category__title": ["icontains"]}
    pagination_class = DefaultPageNumberPagination
    lookup_field = "slug"

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


@extend_schema_view(
    list=extend_schema(
        tags=["Blogs"],
        summary="Get List of all blogs",
        description="Retrieve a paginated list of blogs.",
    ),
    retrieve=extend_schema(
        tags=["Projects"],
        summary="Get Details of a project.",
        description="Retrieve a project with its details.",
    ),
)
class BlogViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPageNumberPagination
    lookup_field = "slug"

    def get_queryset(self):
        if self.action == "list":
            return Blog.objects.filter(status=Blog.BlogStatus.PUBLISHED)
        elif self.action == "retrieve":

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
    summary="Create a new comment/reply",
    description="Create a new comment or reply for a given blog and returns response 201",
)
class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        blog = self.get_blog()
        parent = self.get_parent()

        if parent and parent.blog != blog:
            raise ValidationError(_("Parent comment does not belong to this blog"))

        serializer.save(blog=blog, parent=parent)

    def get_blog(self):
        blog_slug = self.kwargs.get("blog_slug")
        print(blog_slug)
        return get_object_or_404(Blog, slug=blog_slug)

    def get_parent(self):
        parent_pk = self.request.data.get("parent")
        if parent_pk:
            try:
                return Comment.objects.get(pk=parent_pk)
            except Comment.DoesNotExist:
                raise NotFound(_("Parent comment does not exist."))
        return None
