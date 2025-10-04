from django.urls import path

from . import views

urlpatterns = [
    path("projects/", views.ProjectListAPIView.as_view(), name="list-projects"),
    path(
        "projects/<slug:slug>/",
        views.ProjectDetailsAPIView.as_view(),
        name="details-projects",
    ),
    path("blogs/", views.BlogListAPIView.as_view(), name="list-blogs"),
    path(
        "blogs/<slug:slug>/", views.BlogDetailsAPIView.as_view(), name="details-blogs"
    ),
    path(
        "blogs/<slug:slug>/comment/",
        views.CommentCreateAPIView.as_view(),
        name="create-comment",
    ),
    path(
        "blogs/<slug:slug>/comment/<int:pk>/reply/",
        views.ReplyCreateAPIView.as_view(),
        name="create-reply",
    ),
]
