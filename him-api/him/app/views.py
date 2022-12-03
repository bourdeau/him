from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from him.settings import config
from random import randint

from him.app.serializers import PersonSerializer, MessageTemplateSerializer
from him.app.models import Person, MessageTemplate
from him.app.bot import TinderBot


@api_view(["GET"])
def bot_like_profiles(request):
    if config["env"]["like"]:
        rand_like = randint(0, 1)
        if rand_like == 1:
            bot = TinderBot()
            bot.like_profiles()

    return Response({"message": "Liked profiles"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def bot_send_first_messages(request):
    bot = TinderBot()
    bot.send_first_messages()

    return Response({"message": "First messages sent"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def bot_chat_with_matches(request):
    if config["env"]["chat"]:
        rand_chat = randint(0, 10)
        if rand_chat > 6:
            bot = TinderBot()
            bot.chat_with_matches()

    return Response({"message": "Chated with Matches"}, status=status.HTTP_200_OK)


class PersonViewSet(viewsets.ModelViewSet):
    """
    PersonViewSet.
    """

    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """
    MessageTemplate.
    """

    permission_classes = [IsAuthenticated]
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
