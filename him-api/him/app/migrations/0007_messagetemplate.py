# Generated by Django 4.1.3 on 2022-12-01 13:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_person_phone_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="MessageTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "message_template",
                "ordering": ["created_at"],
            },
        ),
    ]
