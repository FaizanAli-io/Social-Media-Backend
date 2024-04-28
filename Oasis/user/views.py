from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm

from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from core.models import User, FriendRequest
from notification.utils import create_notification

from .forms import SignupForm, ProfileForm
from .serializers import UserSerializer, FriendRequestSerializer


@api_view(["GET"])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    friends = user.friends.all()

    requests = (
        FriendRequest.objects.filter(
            created_for=request.user,
            status=FriendRequest.SENT,
        )
        if user == request.user
        else []
    )

    return Response(
        {
            "user": UserSerializer(user).data,
            "friends": UserSerializer(friends, many=True).data,
            "requests": FriendRequestSerializer(requests, many=True).data,
        }
    )


@api_view(["GET"])
def friend_suggestions(request):
    suggestions = request.user.people_you_may_know.all()
    return Response(UserSerializer(suggestions, many=True).data)


@api_view(["POST"])
def send_friend_request(request, pk):
    user = User.objects.get(pk=pk)

    can_request = not FriendRequest.objects.filter(
        Q(created_for=request.user, created_by=user)
        | Q(created_for=user, created_by=request.user)
    ).exists()

    if can_request:
        friend_request = FriendRequest.objects.create(
            created_by=request.user, created_for=user
        )
        message = "friend request created"

        create_notification(request, "sentrequest", friend_request_id=friend_request.id)

    else:
        message = "friend request already exists"

    return Response({"message": message})


@api_view(["POST"])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friend_request = FriendRequest.objects.filter(created_for=request.user).get(
        created_by=user
    )
    friend_request.status = status
    friend_request.save()

    user.friends.add(request.user)
    request.user.friend_count += 1
    user.friend_count += 1

    request.user.save()
    user.save()

    create_notification(
        request,
        f"{status}request",
        friend_request_id=friend_request.id,
    )

    return Response({"message": "friend request updated"})


@api_view(["GET"])
def me(request):
    return Response(
        {
            "id": request.user.id,
            "name": request.user.name,
            "email": request.user.email,
            "avatar": request.user.avatar_url(),
        }
    )


@api_view(["POST"])
def edit_profile(request):
    user = request.user

    email = request.data.get("email")

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({"message": "email already exists"})

    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

        return Response({"message": "success", "user": UserSerializer(user).data})


@api_view(["POST"])
def edit_password(request):
    form = PasswordChangeForm(data=request.POST, user=request.user)

    if form.is_valid():
        form.save()
        return Response({"message": "success"})

    else:
        return Response({"message": form.errors.as_json()})


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def signup(request):
    data = request.data
    message = "success"

    form = SignupForm(
        {
            "name": data.get("name"),
            "email": data.get("email"),
            "password1": data.get("password1"),
            "password2": data.get("password2"),
        }
    )

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        url = (
            f"{settings.WEBSITE_URL}api/activateemail/?email={user.email}&id={user.id}"
        )

        send_mail(
            "Verify your account",
            f"To verify your account click on the following url: {url}",
            "noreply@example.com",
            [user.email],
            fail_silently=False,
        )

    else:
        message = form.errors.as_json()

    return Response({"message": message})


def activate_email(request):
    id = request.GET.get("id", "")
    email = request.GET.get("email", "")

    if id and email:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()

    return Response(f"Thank you for activating your account {user.name}")
