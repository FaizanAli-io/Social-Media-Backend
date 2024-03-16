from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.post_list_feed, name="post-list-feed"),
    path("create/", views.post_create, name="post-create"),
    path("<uuid:id>", views.post_detail, name="post-detail"),
    path("<uuid:id>/like/", views.post_like, name="post-like"),
    path("<uuid:id>/comment/", views.post_comment, name="post-comment"),
    path("profile/<uuid:id>/", views.post_list_profile, name="post-profile"),
    path("trends/", include("trends.urls")),
]
