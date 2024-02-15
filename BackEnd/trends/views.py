from django.utils import timezone
from django.http import JsonResponse

from rest_framework import serializers
from rest_framework.decorators import api_view

from .models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ['id', 'content', 'occurrence', 'modified_at']


@api_view(['GET'])
def get_trending(request):
    yesterday = timezone.now() - timezone.timedelta(1)
    objects = Hashtag.objects.filter(modified_at__gte=yesterday)[:5]
    serializer = HashtagSerializer(objects, many=True)
    return JsonResponse(serializer.data, safe=False)
