from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import Blog, Category, Comment, GalleryItem, Project

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "projects_count"]
    search_fields = ["title"]

    @admin.display(ordering="projects_count")
    def projects_count(self, obj):
        return obj.projects.count()

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(projects_count=Count("projects"))


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    readonly_fields = ["slug", "created_at"]
    list_display = ["title", "slug", "category__title", "status", "created_at"]
    list_editable = ["status"]
    list_filter = ["status", "category"]
    search_fields = ["title"]
    search_help_text = _("Search for project via title")
    list_select_related = ["category"]
    list_per_page = 20
    inlines = [GalleryItemInline]


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ["project__title", "image", "created_at"]
    list_filter = ["project__title"]
    list_select_related = ["project"]
    list_per_page = 20


class CommentInline(admin.StackedInline):
    model = Comment
    fields = ["name", "email", "text", "parent", "status"]
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "status", "created_at", "updated_at"]
    readonly_fields = ["slug", "created_at", "updated_at"]
    list_filter = ["status"]
    list_editable = ["status"]
    list_per_page = 20
    search_fields = ["title"]
    inlines = [CommentInline]
    search_fields = ["title"]
    search_help_text = _("Search for project via title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "blog__id", "parent__id", "status", "created_at"]
    search_fields = ["id"]
    autocomplete_fields = ["blog", "parent"]
    list_per_page = 20
    list_editable = ["status"]
