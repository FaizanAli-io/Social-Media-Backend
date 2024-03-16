from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User, FriendRequest
from account.serializers import UserSerializer

from trends.scripts import add_hashtags
from notification.utils import create_notification

from .models import Post, Like, Comment

from .serializers import (
    PostSerializer,
    CommentSerializer,
)

from .forms import PostForm, AttachmentForm


@api_view(["GET"])
def post_list_feed(request):
    valid_ids = [request.user.id] + [user.id for user in request.user.friends.all()]
    posts = Post.objects.filter(created_by_id__in=valid_ids)

    trend = request.GET.get("trend", "")
    if trend:
        posts = Post.objects.filter(body__icontains=trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_detail(request, id):
    valid_ids = [request.user.id] + [user.id for user in request.user.friends.all()]
    post = Post.objects.filter(
        Q(created_by_id__in=valid_ids) | Q(is_private=False)
    ).get(pk=id)

    serializer = PostSerializer(post)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by=user)
    if request.user.id != user.id:
        if request.user not in user.friends.all():
            posts = posts.filter(is_private=False)

    user_serializer = UserSerializer(user)
    post_serializer = PostSerializer(posts, many=True)

    can_request = True

    check1 = FriendRequest.objects.filter(
        created_for=request.user, created_by=user
    ).exists()
    check2 = FriendRequest.objects.filter(
        created_for=user, created_by=request.user
    ).exists()

    if check1 or check2:
        can_request = False

    return JsonResponse(
        {
            "can_request": can_request,
            "user": user_serializer.data,
            "posts": post_serializer.data,
        },
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    attachment = None
    post_form = PostForm(request.POST)
    attachment_form = AttachmentForm(request.POST, request.FILES)

    print("start", post_form.data, "stop")

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        request.user.post_count += 1
        request.user.save()

        if not post.is_private:
            add_hashtags(post.body)

        return JsonResponse(PostSerializer(post).data, safe=False)

    else:
        return JsonResponse({"error": "post not created"})


@api_view(["POST"])
def post_like(request, id):
    post = Post.objects.get(id=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post.like_count += 1
        post.likes.add(like)
        post.save()

        create_notification(request, "postlike", post_id=post.id)

        message = "like created"
    else:
        message = "already liked"

    return JsonResponse({"message": message})


@api_view(["POST"])
def post_comment(request, id):
    comment = Comment.objects.create(
        body=request.data.get("body"),
        created_by=request.user,
    )

    post = Post.objects.get(id=id)
    post.comments.add(comment)
    post.comment_count += 1
    post.save()

    create_notification(request, "postcomment", post_id=post.id)

    return JsonResponse(CommentSerializer(comment).data, safe=False)
