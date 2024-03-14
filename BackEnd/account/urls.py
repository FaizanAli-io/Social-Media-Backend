from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("me/", views.me, name="me"),
    path("signup/", views.signup, name="signup"),
    path("editprofile/", views.edit_profile, name="edit-profile"),
    path("editpassword/", views.edit_password, name="edit-password"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("signin/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("activateemail/", views.activate_email, name="activate-email"),
    path("friends/<uuid:pk>/", views.friends, name="friends"),
    path(
        "friends/<uuid:pk>/request/",
        views.send_friend_request,
        name="send-friend-request",
    ),
    path(
        "friends/<uuid:pk>/<str:status>/",
        views.handle_request,
        name="handle-request",
    ),
]
