from django.db import models


class Personn(models.Model):
    """
    Personn model
    """
    id = models.TextField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.TextField(null=False)
    gender = models.IntegerField(null=False)
    bio = models.TextField(null=True)
    distance_mi = models.IntegerField(null=True)
    birth_date = models.DateTimeField(null=True)
    liked = models.BooleanField(null=True)

    class Meta:
        db_table = "personn"
        ordering = ["created_at"]


class Photo(models.Model):
    """
    Photo model
    """
    id = models.TextField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    url = models.TextField(null=False)
    score = models.FloatField(null=True)
    personn = models.ForeignKey(Personn, on_delete=models.CASCADE)

    class Meta:
        db_table = "photo"
        ordering = ["created_at"]
