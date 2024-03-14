from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.notifications, name="notifications"),
    path("read/<uuid:pk>", views.read_notification, name="read-notifications"),
]
