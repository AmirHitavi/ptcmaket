from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Blog, Category, Comment, GalleryItem, Project


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["title", "get_projects_count"]
    search_fields = ["title"]

    @admin.display(ordering="projects_count", description=_("Projects"))
    def get_projects_count(self, obj):
        return getattr(obj, "projects_count", 0)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(projects_count=Count("projects"))


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 1


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    autocomplete_fields = ["category"]
    readonly_fields = ["slug", "created_at"]
    list_display = ["title", "slug", "get_category_title", "status", "created_at"]
    list_editable = ["status"]
    list_filter = ["status", "category"]
    search_fields = ["title"]
    search_help_text = _("Search for project via title")
    list_select_related = ["category"]
    list_per_page = 20
    inlines = [GalleryItemInline]

    @admin.display(ordering="category__title", description=_("Category"))
    def get_category_title(self, obj: Project):
        return obj.category.title if obj.category else "-"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ["get_project_title", "image", "created_at"]
    list_filter = ["project__title"]
    list_select_related = ["project"]
    list_per_page = 20

    @admin.display(ordering="project__title", description=_("Project"))
    def get_project_title(self, obj: GalleryItem):
        return obj.project.title


class CommentInline(admin.StackedInline):
    model = Comment
    fields = ["name", "email", "text", "parent", "status"]
    extra = 0


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = [
        "title",
        "slug",
        "status",
        "comments_count",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["slug", "created_at", "updated_at"]
    list_filter = ["status"]
    list_editable = ["status"]
    list_per_page = 20
    search_fields = ["title"]
    inlines = [CommentInline]
    search_fields = ["title"]
    search_help_text = _("Search for project via title")

    @admin.display(ordering="comments_count", description=_("Comments"))
    def comments_count(self, obj):
        return getattr(obj, "comments_count", 0)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(comments_count=Count("comments"))


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "get_blog_id",
        "get_parent_id",
        "status",
        "created_at",
    ]
    search_fields = ["id"]
    autocomplete_fields = ["blog", "parent"]
    list_per_page = 20
    list_editable = ["status"]
    list_select_related = ["parent", "blog"]

    @admin.display(ordering="blog__id", description=_("Blog"))
    def get_blog_id(self, obj: Comment):
        return obj.blog.id

    @admin.display(ordering="parent__id", description=_("Parent"))
    def get_parent_id(self, obj: Comment):
        return obj.parent.id if obj.parent else "-"
