# Generated by Django 4.1.3 on 2022-11-29 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='person',
        ),
        migrations.AddField(
            model_name='message',
            name='sent_from',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sent_from', to='app.person'),
        ),
        migrations.AddField(
            model_name='message',
            name='sent_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sent_to', to='app.person'),
        ),
    ]