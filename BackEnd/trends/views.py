from django.http import JsonResponse

from rest_framework import serializers
from rest_framework.decorators import api_view

from .models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ['content', 'occurrence']


@api_view(['GET'])
def get_trending(request):
    objects = Hashtag.objects.all()[:5]
    serializer = HashtagSerializer(objects, many=True)
    return JsonResponse(serializer.data, safe=False)
