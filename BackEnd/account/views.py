from django.http import JsonResponse

from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    api_view,
)

from .forms import SignupForm

from .models import (
    User,
    FriendRequest,
)

from .serializers import (
    UserSerializer,
    FriendRequestSerializer,
)


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    friends = user.friends.all()
    requests = FriendRequest.objects.filter(
        created_for=request.user,
        status=FriendRequest.SENT,
    ) if user == request.user else []

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendRequestSerializer(requests, many=True).data,
    }, safe=False)


@api_view(['POST'])
def send_friend_request(request, pk):
    user = User.objects.get(pk=pk)
    check1 = FriendRequest.objects.filter(
        created_for=request.user, created_by=user)
    check2 = FriendRequest.objects.filter(
        created_for=user, created_by=request.user)

    if not (check1 or check2):
        FriendRequest.objects.create(
            created_by=request.user,
            created_for=user)
        message = 'friend request created'
    else:
        message = 'friend request already exists'

    return JsonResponse({'message': message})


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendRequest = FriendRequest.objects.filter(
        created_for=request.user).get(created_by=user)
    friendRequest.status = status
    friendRequest.save()

    user.friends.add(request.user)
    request.user.friend_count += 1
    user.friend_count += 1

    request.user.save()
    user.save()

    return JsonResponse({'message': 'friend request updated'})


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'name': data.get('name'),
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
    else:
        message = 'error'

    return JsonResponse({'message': message})
