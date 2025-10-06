from django.urls import path

from . import views

urlpatterns = [
    path(
        "contact/",
        views.ContactViewSet.as_view({"post": "create"}),
        name="create-contact",
    ),
    path("order/", views.OrderViewSet.as_view({"post": "create"}), name="create-order"),
    path(
        "apply-application/",
        views.ApplyApplicationViewSet.as_view({"post": "create"}),
        name="create-apply-application",
    ),
]
