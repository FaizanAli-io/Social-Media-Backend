from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User
from account.serializers import UserSerializer

from post.models import Post
from post.serializers import PostSerializer


@api_view(["POST"])
def search(request):
    query = request.data["query"]

    users = User.objects.filter(name__icontains=query)
    posts = Post.objects.filter(body__icontains=query)

    valid_ids = [request.user.id] + [user.id for user in request.user.friends.all()]
    posts = posts.filter(Q(created_by_id__in=valid_ids) | Q(is_private=False))

    user_serializer = UserSerializer(users, many=True)
    post_serializer = PostSerializer(posts, many=True)

    return JsonResponse(
        {
            "users": user_serializer.data,
            "posts": post_serializer.data,
        },
        safe=False,
    )
