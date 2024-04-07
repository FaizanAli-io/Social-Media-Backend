from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.serializers import UserSerializer
from notification.utils import create_notification
from core.models import User, FriendRequest, Post, Like, Comment, Hashtag

from .forms import PostForm, AttachmentForm
from .serializers import PostSerializer, CommentSerializer, HashtagSerializer


@api_view(["GET"])
def post_list_feed(request):
    valid_ids = [request.user.pk] + [user.pk for user in request.user.friends.all()]
    posts = Post.objects.filter(created_by_id__in=valid_ids)

    trend = request.GET.get("trend", "")
    if trend:
        posts = Post.objects.filter(body__icontains=trend).filter(is_private=False)

    return Response(PostSerializer(posts, many=True).data)


@api_view(["GET"])
def post_list_profile(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(created_by=user)
    if request.user.pk != user.pk:
        if request.user not in user.friends.all():
            posts = posts.filter(is_private=False)

    can_request = not FriendRequest.objects.filter(
        Q(created_for=request.user, created_by=user)
        | Q(created_for=user, created_by=request.user)
    ).exists()

    return Response(
        {
            "can_request": can_request,
            "user": UserSerializer(user).data,
            "posts": PostSerializer(posts, many=True).data,
        }
    )


@api_view(["POST"])
def post_create(request):
    attachment = None
    post_form = PostForm(request.POST)
    attachment_form = AttachmentForm(request.POST, request.FILES)

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

        return Response(PostSerializer(post).data)

    else:
        return Response({"error": "post not created"})


@api_view(["GET"])
def post_detail(request, pk):
    valid_ids = [request.user.pk] + [user.pk for user in request.user.friends.all()]
    post = Post.objects.filter(
        Q(created_by_id__in=valid_ids) | Q(is_private=False)
    ).get(pk=pk)

    return Response(PostSerializer(post).data)


@api_view(["POST"])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post.like_count += 1
        post.likes.add(like)
        post.save()

        create_notification(request, "postlike", post_id=post.pk)

        message = "like created"
    else:
        message = "already liked"

    return Response({"message": message})


@api_view(["POST"])
def post_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get("body"),
        created_by=request.user,
    )

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comment_count += 1
    post.save()

    create_notification(request, "postcomment", post_id=post.pk)

    return Response(CommentSerializer(comment).data)


@api_view(["POST"])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by.add(request.user)
    post.save()

    return Response({"message": "Post reported successfully."})


@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)

    if post.created_by.pk != request.user.pk:
        message = "You cannot delete someone elses post."
        status = "failure"

    else:
        message = "Post deleted successfully."
        request.user.post_count -= 1
        request.user.save()
        status = "success"
        post.delete()

    return Response({"status": status, "message": message})


@api_view(["GET"])
def get_trending(_):
    objects = Hashtag.objects.filter()[:10]
    return Response(HashtagSerializer(objects, many=True).data)
