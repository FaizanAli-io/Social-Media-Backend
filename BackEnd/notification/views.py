from django.http import JsonResponse

from core.models import Notification

from rest_framework.decorators import api_view

from .serializers import NotificationSerializer


@api_view(["GET"])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def read_notification(request, pk):
    notif = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notif.is_read = True
    notif.save()

    return JsonResponse({"message": "notification read"})
