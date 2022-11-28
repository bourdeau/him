from rest_framework import viewsets
from him.app.serializers import PersonnSerializer

from him.app.models import Personn


class PersonnViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Personn.objects.all()
    serializer_class = PersonnSerializer

class BotViewSet(viewsets.ViewSet):
    def list(self, request):
        pass