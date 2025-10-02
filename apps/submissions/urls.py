from django.urls import path

from . import views

urlpatterns = [
    path("contact/", views.ContactAPIView.as_view(), name="create-contact"),
    path("order/", views.OrderAPIView.as_view(), name="create-order"),
    path(
        "apply-application/",
        views.ApplyApplicationAPIView.as_view(),
        name="create-apply-application",
    ),
]
