# Generated by Django 4.1.3 on 2022-11-30 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_message_options_alter_photo_person"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="order_id",
        ),
    ]
