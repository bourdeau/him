# Generated by Django 4.1.3 on 2022-12-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_messagetemplate_nb_reply_messagetemplate_nb_sent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="messagetemplate",
            name="nb_reply",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="messagetemplate",
            name="nb_sent",
            field=models.IntegerField(default=0),
        ),
    ]
