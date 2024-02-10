from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User

from .models import (
    Conversation,
    ConversationMessage,
)

from .serializers import (
    ConversationSerializer,
    ConversationMessageSerializer,
    ConversationDetailSerializer,
)


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=[request.user])
    serializer = ConversationSerializer(conversations, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def start_convo(request, pk):
    receiver = User.objects.get(pk=pk)
    conversations = Conversation.objects.filter(
        users__in=[request.user]).filter(
            users__in=[receiver])

    if conversations.exists():
        conversation = conversations.first()
        created = False
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(receiver, request.user)
        conversation.save()
        created = True

    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse({
        'conversation': serializer.data,
        'created': created,
    })


@api_view(['POST'])
def send_message(request, pk):
    conversation = Conversation.objects.filter(
        users__in=[request.user]).get(pk=pk)

    for user in conversation.users.all():
        if user.id != request.user.id:
            receiver = user

    message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data['body'],
        sent_by=request.user,
        sent_to=receiver,
    )

    serializer = ConversationMessageSerializer(message)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(
        users__in=[request.user]).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)
