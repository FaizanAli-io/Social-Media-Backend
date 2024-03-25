from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListUpdateNotificationAPIView.as_view(), name="notifications"),
]
