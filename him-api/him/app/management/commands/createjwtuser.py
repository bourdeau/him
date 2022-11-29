from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a JWT user"

    def add_arguments(self, parser):
        parser.add_argument("--name", type=str)
        parser.add_argument("--email", type=str)
        parser.add_argument("--password", type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_superuser(
            options["name"], options["email"], options["password"]
        )

        self.stdout.write(self.style.SUCCESS("Success"))
