from random import randint
from him.settings import config
from django.db.models import Q
from him.app.helpers import Base
from him.app.message import MessageTemplate
from him.app.models import Person, Message
from him.app.serializers import MatchAPISerializer
from him.app.chat import Chat
from him.app.helpers import find_phone_number


class TinderBot(Base):
    def __init__(self) -> None:
        super().__init__()

        self.current_like = 0

    def like_profiles(self) -> None:
        """
        Liking profiles.
        """
        self.sleep_long()
        self.logger.info("❤️ ❤️ ❤️  LIKING PROFILES ❤️ ❤️ ❤️")

        nb_profile_to_like = randint(10, 50)

        while self.current_like < nb_profile_to_like:
            persons_data = self.tinderapi.get_likables()

            if not persons_data:
                self.logger.info("No profiles to Like found")
                return

            for person_data in persons_data:
                self.sleep_long()
                person = person_data.save()
                likable = person.likable()
                if likable:
                    self.current_like += 1
                    self.tinderapi.like(person.id)
                    message = "liked"
                else:
                    self.tinderapi.dislike(person.id)
                    message = "disliked"

                person.save()

                self.logger.info(f"👤 {person.name}: {message}")

    def send_first_messages(self) -> None:
        """
        Send first message to all the new matches in the left panel.
        """
        self.logger.info("✉️ ✉️ ✉️ SENDING FIRST MESSAGE ✉️ ✉️ ✉️")

        new_matches = self.tinderapi.get_new_matches()

        if not new_matches:
            self.logger.info("No profiles to Like found")
            return

        for match_id, personn_id, person_name in new_matches:
            self.sleep_long()
            message = MessageTemplate()
            message = message.get_message(person_name)
            self.tinderapi.send_message(match_id, personn_id, message)

            self.logger.info("✉️ sent to %s : %s", person_name, message)

    def chat_with_matches(self):
        """
        Chat with all the matches in the left panel.
        """
        self.logger.info("💬 💬 💬  CHATING WITH MATCHES 💬 💬 💬")
        matches = self.tinderapi.get_matches()

        if not matches:
            self.logger.info("No matches found")
            return

        for match in matches:
            match_id = match.data["id"]  # TODO match.validated
            messages = self.tinderapi.get_messages(match_id)

            self.__save_message_to_db(messages)
            self.__chat_with_a_match(match)

    def __save_message_to_db(self, messages: list) -> None:
        """
        Save the message in the database.
        """
        for message in messages:
            message = message.validated_data

            try:
                sent_from = Person.objects.get(pk=message["sent_from"])
            except Person.DoesNotExist:
                person_data = self.tinderapi.get_profile(message["sent_from"])
                sent_from = person_data.save()

            try:
                sent_to = Person.objects.get(pk=message["sent_to"])
            except Person.DoesNotExist:
                person_data = self.tinderapi.get_profile(message["sent_to"])
                sent_to = person_data.save()

            # If a phone number is found in a message
            if sent_from.id != config["your_profile"]["id"]:
                phone_number = find_phone_number(message["message"])
                if phone_number:
                    sent_from.phone_number = phone_number
                    sent_from.whitelist = True
                    sent_from.save()
                    self.logger.info(f"📞 Phone number {phone_number} found")

            message["sent_from"] = sent_from
            message["sent_to"] = sent_to

            try:
                message = Message.objects.get(pk=message["id"])
            except Message.DoesNotExist:
                message = Message(**message)
                message.save()

    def __chat_with_a_match(self, match: MatchAPISerializer) -> None:
        """
        Build a chat_history with the match for the Chat blot.
        """
        match = match.validated_data
        id_person = match["person"]["id"]

        person = Person.objects.get(pk=id_person)

        chat_history = {
            "her": {
                "id": person.id,
                "match_id": match["id"],
                "name": person.name,
                "bio": person.bio,
                "whitelist": person.whitelist,
            },
            "chat_history": [],
        }

        messages = Message.objects.filter(Q(sent_from=id_person) | Q(sent_to=id_person))

        for message in messages:
            if message.sent_from.id == id_person:
                name = person.name
            else:
                name = "Pierre"

            message = {
                "user": name,
                "message": message.message,
            }
            chat_history["chat_history"].append(message)

        chat = Chat()
        chat.chat(chat_history)
