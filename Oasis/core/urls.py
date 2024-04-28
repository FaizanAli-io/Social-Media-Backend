from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_command_list, name="command-list"),
    path("<str:command>", views.run_command, name="run-command"),
]
