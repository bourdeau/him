from rest_framework import serializers
from him.app.models import Person, Photo


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


# API Serializers
class PhotoAPISerializer(serializers.Serializer):

    id = serializers.CharField()
    url = serializers.CharField()
    score = serializers.FloatField(required=False)


class PersonAPISerializer(serializers.Serializer):

    _id = serializers.CharField(source="id")
    name = serializers.CharField(required=True, allow_blank=True)
    bio = serializers.CharField(
        required=False,
        max_length=None,
        min_length=None,
        allow_blank=True,
        trim_whitespace=True,
    )
    birth_date = serializers.DateTimeField(
        required=False, input_formats=["iso-8601"], format="Y-m-d"
    )
    distance_mi = serializers.IntegerField(required=False)
    gender = serializers.IntegerField()
    photos = PhotoAPISerializer(required=False, many=True)

    def create(self, validated_data):
        photos_data = validated_data.pop("photos")

        person = Person(**validated_data)
        person.save()

        for photo_data in photos_data:
            photo = Photo(**photo_data)
            photo.person = person
            photo.save()
            person.photo_set.add(photo)

        return person


class MatchAPISerializer(serializers.Serializer):

    id = serializers.CharField()
    person = PersonAPISerializer(required=True)


class MessageAPISerializer(serializers.Serializer):

    _id = serializers.CharField(source="id")
    sent_date = serializers.DateTimeField()
    sent_from = serializers.CharField()
    to = serializers.CharField()
    message = serializers.CharField()

    def get_fields(self):
        result = super().get_fields()
        sent_from = result.pop("sent_from")
        result["from"] = sent_from

        return result