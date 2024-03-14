from rest_framework.serializers import ModelSerializer

from .models import Notification


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ["id", "body", "post_id", "created_for_id", "notification_type"]
