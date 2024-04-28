from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.management import call_command

COMMAND_LIST = [
    # (function name, human readable name)
    ("generate_trends", "Generate Trends"),
    ("suggest_friends", "Suggest Friends"),
]


@api_view(["GET"])
def get_command_list(request):
    return Response(COMMAND_LIST if request.user.is_superuser else [])


@api_view(["GET"])
def run_command(_, command):
    command_names = [cmd[0] for cmd in COMMAND_LIST]
    if command in command_names:
        call_command(command)
        return Response(f"Successfully Called '{command}'")
    return Response("Invalid Command", status=status.HTTP_400_BAD_REQUEST)
