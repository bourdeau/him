from django.core.management.base import BaseCommand
from him.app.bot import TinderBot


class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **options):
        bot = TinderBot()
        bot.run()
