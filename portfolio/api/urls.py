from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("projects", views.ProjectViewSet, basename="projects")
router.register("blogs", views.BlogViewSet, basename="blogs")

blog_router = routers.NestedDefaultRouter(router, "blogs", lookup="blog")
urlpatterns = [
    *router.urls,
    *blog_router.urls,
    path(
        "blogs/<slug:blog_slug>/comment/",
        views.CommentViewSet.as_view({"post": "create"}),
        name="blog-comment-create",
    ),
]
