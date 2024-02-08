from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('create/', views.post_create, name='post-create'),
    path('<uuid:id>/like/', views.post_like, name='post-like'),
    path('profile/<uuid:id>/', views.post_list_profile, name='post-list-profile'),
]
