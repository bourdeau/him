import uuid
from django.db import models
from him.settings import config


class Person(models.Model):
    """
    Person model
    """

    id = models.TextField(primary_key=True)
    name = models.TextField(null=False)
    gender = models.IntegerField(null=False)
    birth_date = models.DateField(null=True)
    distance_mi = models.IntegerField(null=True)
    liked = models.BooleanField(null=False, default=True)
    match = models.BooleanField(null=False, default=False)
    whitelist = models.BooleanField(null=False, default=False)
    bio = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "person"
        ordering = ["created_at"]

    def likable(self):
        """
        Check if a person is likable
        """
        if self.distance_mi <= config["like"]["radius"]:
            self.liked = True
            return True

        self.liked = False

        return False

class Match(models.Model):
    """
    Match model.

    Example:
    {
        "id": "5eb99066d967c501009b059962d7d7a14e95f00100f1cc19",
        "closed": False,
        "common_like_count": 0,
        "created_date": "2022-12-02T10:10:33.128Z",
        "dead": False,
        "last_activity_date": "2022-12-05T12:17:32.160Z",
        "message_count": 0,
        "pending": False,
        "is_super_like": False,
        "is_boost_match": False,
        "is_super_boost_match": False,
        "is_primetime_boost_match": False,
        "is_experiences_match": False,
        "is_fast_match": False,
        "is_preferences_match": False,
        "is_matchmaker_match": False,
        "is_opener": True,
        "has_shown_initial_interest": True,
        "person": {},
        "following": True,
        "following_moments": True,
        "subscription_tier": "platinum",
        "is_archived": False,
    }
    """

    id = models.TextField(primary_key=True)
    person_1 = models.ForeignKey(Person, related_name="person_1", on_delete=models.CASCADE)
    person_2 = models.ForeignKey(Person, related_name="person_2", on_delete=models.CASCADE)
    closed = models.BooleanField(null=False, default=False)
    common_like_count = models.IntegerField(null=False, default=0)
    created_date = models.DateTimeField(null=True)
    dead = models.BooleanField(null=False, default=False)
    last_activity_date = models.DateTimeField(null=True)
    message_count = models.IntegerField(null=False, default=0)
    pending = models.BooleanField(null=False, default=False)
    is_super_like = models.BooleanField(null=False, default=False)
    is_boost_match = models.BooleanField(null=False, default=False)
    is_super_boost_match = models.BooleanField(null=False, default=False)
    is_primetime_boost_match = models.BooleanField(null=False, default=False)
    is_experiences_match = models.BooleanField(null=False, default=False)
    is_fast_match = models.BooleanField(null=False, default=False)
    is_preferences_match = models.BooleanField(null=False, default=False)
    is_matchmaker_match = models.BooleanField(null=False, default=False)
    is_opener = models.BooleanField(null=False, default=False)
    has_shown_initial_interest = models.BooleanField(null=False, default=False)
    following = models.BooleanField(null=False, default=False)
    following_moments = models.BooleanField(null=False, default=False)
    subscription_tier = models.TextField(null=True, default="platinum")
    is_archived = models.BooleanField(null=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "match"
        ordering = ["created_at"]


class Photo(models.Model):
    """
    Photo model
    """

    id = models.TextField(primary_key=True)
    person = models.ForeignKey(Person, related_name="person", on_delete=models.CASCADE)
    url = models.TextField(null=False)
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "photo"
        ordering = ["created_at"]


class Message(models.Model):
    """
    Message model
    """

    id = models.TextField(primary_key=True)
    match = models.ForeignKey(Match, default=None, related_name="match", on_delete=models.CASCADE)
    sent_from = models.ForeignKey(
        Person, default=None, related_name="sent_from", on_delete=models.CASCADE
    )
    sent_to = models.ForeignKey(
        Person, default=None, related_name="sent_to", on_delete=models.CASCADE
    )
    sent_date = models.DateTimeField(null=True)
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "message"
        ordering = ["sent_date"]


class MessageTemplate(models.Model):
    """
    MessageTemplate model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField(null=False)
    nb_sent = models.IntegerField(null=False, default=0)
    nb_reply = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "message_template"
        ordering = ["created_at"]


