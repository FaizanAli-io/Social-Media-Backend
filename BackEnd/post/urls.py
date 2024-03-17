from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.post_list_feed, name="post-list-feed"),
    path("create/", views.post_create, name="post-create"),
    path("<uuid:pk>", views.post_detail, name="post-detail"),
    path("<uuid:pk>/like/", views.post_like, name="post-like"),
    path("<uuid:pk>/report/", views.post_report, name="post-report"),
    path("<uuid:pk>/delete/", views.post_delete, name="post-delete"),
    path("<uuid:pk>/comment/", views.post_comment, name="post-comment"),
    path("profile/<uuid:pk>/", views.post_list_profile, name="post-profile"),
    path("trends/", include("trends.urls")),
]
