from rest_framework import serializers
from him.app.models import Person, Photo, Message, MessageTemplate, Match
from him.settings import config
import re



class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(required=False, source="person", many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "gender",
            "birth_date",
            "distance_mi",
            "liked",
            "whitelist",
            "bio",
            "messages",
            "photos",
            "created_at",
            "updated_at",
        ]

    def get_messages(self, obj):
        messages = obj.sent_from.all() | obj.sent_to.all()
        return MessageSerializer(messages, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["messages"] = self.get_messages(instance)
        return representation


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
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

        return person


class MatchAPISerializer(serializers.Serializer):
    """
    MatchAPISerializer.
    """
    id = serializers.CharField()
    closed = serializers.BooleanField()
    common_like_count = serializers.IntegerField()
    created_date = serializers.DateTimeField()
    dead = serializers.BooleanField()
    last_activity_date = serializers.DateTimeField()
    message_count = serializers.IntegerField()
    pending = serializers.BooleanField()
    is_super_like = serializers.BooleanField()
    is_boost_match = serializers.BooleanField()
    is_super_boost_match = serializers.BooleanField()
    is_primetime_boost_match = serializers.BooleanField()
    is_experiences_match = serializers.BooleanField()
    is_fast_match = serializers.BooleanField()
    is_preferences_match = serializers.BooleanField()
    is_matchmaker_match = serializers.BooleanField()
    is_opener = serializers.BooleanField()
    has_shown_initial_interest = serializers.BooleanField()
    person = PersonAPISerializer()
    following = serializers.BooleanField()
    following_moments = serializers.BooleanField()
    subscription_tier = serializers.CharField(required=False)
    is_archived = serializers.BooleanField()


    def create(self, validated_data):

        person_2 = validated_data.pop("person")
        person_2.pop("photos")

        try:
            person_2 = Person.objects.get(pk=person_2["id"])
        except Person.DoesNotExist:
            person_2 = Person(**person_2)
        

        person_2.match = True
        person_2.save()

        try:
            person_1 = Person.objects.get(id=config["your_profile"]["id"])
        except Person.DoesNotExist:
            person_1 = Person(id=config["your_profile"]["id"], gender=1, name="Pierre")
            person_1.save()
    

        validated_data["person_1"] = person_1
        validated_data["person_2"] = person_2

        try:
            match = Match.objects.get(pk=validated_data["id"])
        except Match.DoesNotExist:
            match = Match(**validated_data)
            match.save()

        return match


class MessageAPISerializer(serializers.Serializer):

    _id = serializers.CharField(source="id")
    matchId = serializers.CharField(source="match_id")
    sent_date = serializers.DateTimeField()
    sent_from = serializers.CharField()
    sent_to = serializers.CharField()
    message = serializers.CharField()

    def create(self, validated_data):

        match_id = validated_data.pop("match_id")

        match = Match.objects.get(pk=match_id)
        sent_from = Person.objects.get(pk=validated_data["sent_from"])
        sent_to = Person.objects.get(pk=validated_data["sent_to"])


        if sent_from.id != config["your_profile"]["id"]:
            sent_from.match = True
            sent_from.save()

        validated_data["match"] = match
        validated_data["sent_from"] = sent_from
        validated_data["sent_to"] = sent_to

        if sent_from.id != config["your_profile"]["id"] and not sent_from.phone_number:
            phone_number = self.find_phone_number(validated_data["message"])
            if phone_number:
                sent_from.phone_number = phone_number
                sent_from.whitelist = True
                sent_from.save()

        try:
            message = Message.objects.get(pk=validated_data["id"])
        except Message.DoesNotExist:
            message = Message(**validated_data)
            message.save()

        return message


    def find_phone_number(self, text: str):
        """
        Find a French phone number in a string.
        """
        phone = re.search(
            r"(\+33|0)[\s]?[6|7][\s]?[0-9]{2}[\s]?[0-9]{2}[\s]?[0-9]{2}[\s]?[0-9]{2}", text
        )

        if phone:
            return phone.group()

        return None
