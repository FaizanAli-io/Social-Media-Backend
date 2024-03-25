from rest_framework import generics
from rest_framework.response import Response

from core.models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ListCreateConversationAPIView(generics.ListCreateAPIView):

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def list(self, request):
        queryset = self.queryset.filter(users__in=[request.user])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        receiver = User.objects.get(id=request.data["id"])
        conversation = Conversation.objects.filter(
            users__in=[request.user],
        ).filter(
            users__in=[receiver],
        )

        if conversation.exists():
            conversation = conversation.first()
            created = False

        else:
            conversation = Conversation.objects.create()
            conversation.users.add(request.user, receiver)
            conversation.save()
            created = True

        serializer = self.serializer_class(conversation)
        return Response({"conversation": serializer.data, "created": created})


class SendMessageAPIView(generics.CreateAPIView):

    serializer_class = MessageSerializer

    def create(self, request):
        conversation = Conversation.objects.get(id=request.data["id"])
        for user in conversation.users.all():
            if user.id != request.user.id:
                receiver = user

        message = Message.objects.create(
            conversation=conversation,
            body=request.data["body"],
            sent_by=request.user,
            sent_to=receiver,
        )

        serializer = self.serializer_class(message)
        return Response(serializer.data)
