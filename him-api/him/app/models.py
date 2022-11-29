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
    liked = models.BooleanField(null=False, default=False)
    whitelist = models.BooleanField(null=False, default=False)
    bio = models.TextField(null=True)
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


class Photo(models.Model):
    """
    Photo model
    """

    id = models.TextField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    order_id = models.IntegerField(null=False)
    sent_date = models.DateTimeField(null=True)
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "message"
        ordering = ["created_at"]
