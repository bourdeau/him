from rest_framework import viewsets, views
from rest_framework.response import Response

from him.app.serializers import PersonSerializer
from him.app.models import Person, Message
from him.app.bot import TinderBot


class HealthView(views.APIView):
    def get(self, request, format=None):
        return Response({"status": "Ok"})


class BotView(views.APIView):
    def get(self, request, format=None):
        bot = TinderBot()
        bot.run()
        return Response({"status": "Ok"})


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    # def get_queryset(self):
    #     return Person.objects.annotate(
    #         messages=['test', "bla"]
    #     )