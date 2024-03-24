from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreateConversationAPIView.as_view(), name="list-create"),
    path("send/", views.SendMessageAPIView.as_view(), name="send-message"),
]
