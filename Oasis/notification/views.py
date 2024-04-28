from rest_framework import generics
from rest_framework.response import Response

from core.models import Notification
from .serializers import NotificationSerializer


class ListReadNotificationAPIView(
    generics.ListAPIView,
    generics.UpdateAPIView,
):

    serializer_class = NotificationSerializer

    def list(self, request):
        notifs = request.user.received_notifications.filter(is_read=False)
        return Response(NotificationSerializer(notifs, many=True).data)

    def partial_update(self, request):
        instance = Notification.objects.get(id=request.data["id"])
        instance.is_read = True
        instance.save()

        return Response({"message": "Notification Read."})
