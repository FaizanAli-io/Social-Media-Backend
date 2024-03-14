from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_trending, name="get-trending"),
]
