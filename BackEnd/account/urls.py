from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

# app_name = 'account'

urlpatterns = [
    path('me/', views.me, name='me'),
    path('signup/', views.signup, name='signup'),
    path('signin/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
