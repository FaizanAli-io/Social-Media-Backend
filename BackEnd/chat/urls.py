from django.urls import path

from . import views

urlpatterns = [
    path("", views.conversation_list, name="conversation-list"),
    path("<uuid:pk>/start/", views.start_convo, name="start-convo"),
    path("<uuid:pk>/send/", views.send_message, name="send-message"),
    path("<uuid:pk>/", views.conversation_detail, name="conversation-detail"),
]
