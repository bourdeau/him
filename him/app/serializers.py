from rest_framework import serializers
from him.app.models import Personn


class PersonnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personn
        fields = "__all__"
