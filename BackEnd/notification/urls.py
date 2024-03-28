from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListReadNotificationAPIView.as_view(), name="list-read"),
]
