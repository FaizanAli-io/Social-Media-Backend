from rest_framework import generics, mixins
from rest_framework.response import Response

from .serializers import NotificationSerializer


class ListUpdateNotificationAPIView(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = NotificationSerializer

    def list(self, request):
        notifs = request.user.received_notifications.filter(is_read=False)
        return Response(NotificationSerializer(notifs, many=True).data)

    def update(self):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
