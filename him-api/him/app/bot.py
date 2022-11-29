from him.settings import config

from him.app.helpers import Base
from him.app.message import Message
from him.app.models import Person, Photo, Message


class TinderBot(Base):
    def __init__(self) -> None:
        super().__init__()

        self.current_like = 0

    def run(self) -> None:
        """
        Main function which like profiles and send first message.
        """
        # test = self.tinderapi.get_updates()
        # print(type(test))
        # print(test)

        raise Exception
        if config["env"]["like"]:
            self.__like_profiles()
        if config["env"]["send_first_message"]:
            self.__send_first_messages()
        if config["env"]["chat"]:
            self.__chat_with_matches()

    def __like_profiles(self) -> None:
        """
        Liking new profiles until it reaches MAX_LIKE.
        It also download the first image of the profile.
        """
        self.sleep_long()
        self.logger.info("❤️ ❤️ ❤️  LIKING PROFILES ❤️ ❤️ ❤️")

        while self.current_like < config["like"]["max"]:
            likables = self.tinderapi.get_likables()

            if not likables:
                self.logger.info("No profiles to Like found")
                return

            for likable in likables:
                self.sleep_long()
                self.logger.info("---------------------------------")
                self.logger.info("👤 %s", likable["name"])

                photos = likable["photos"]
                likable.pop("photos", None)
                person = Person(**likable)

                if likable["distance_mi"] <= config["like"]["radius"]:
                    self.tinderapi.like(likable["id"])
                    self.current_like += 1
                    person.liked = True
                    self.logger.info("Liked !")
                else:
                    self.tinderapi.dislike(likable["id"])
                    person.liked = False
                    self.logger.info("Disliked...")

                person.save()

                for photo_data in photos:
                    photo = Photo(**photo_data, person=person)
                    photo.save()

    def __send_first_messages(self) -> None:
        """
        Send first message to all the new matches in the left panel.
        """
        self.logger.info("✉️ ✉️ ✉️ SENDING FIRST MESSAGE ✉️ ✉️ ✉️")

        new_matches = self.tinderapi.get_new_matches()

        for new_match in new_matches:
            message = Message()
            message = message.get_message(profile_name=new_match["name"])
            self.tinderapi.send_message(new_match["id"], message)
            self.logger.info("Message sent to %s : %s", new_match["name"], message)

    def __chat_with_matches(self):
        """
        Chat with all the matches in the left panel.
        """
        self.logger.info("💬 💬 💬  CHATING WITH MATCHES 💬 💬 💬")
        matches = self.tinderapi.get_matches()

        if not matches:
            self.logger.info("No matches found")
            return

        for match in matches:
            messages = self.tinderapi.get_messages(match["id_match"])

            self.__chat_with_a_match(match, messages)

    def __chat_with_a_match(self, match, messages):

        chat_data = {"her": match, "chat_history": []}

        messages.reverse()

        for i, message in enumerate(messages):
            message["order_id"] = i
            self.save_message_to_db(message)

            message_data = {"id": i, "message": message["message"]}

            if message["person"] == chat_data["her"]["id_profile"]:
                message_data["user"] = chat_data["her"]["name"]
            else:
                message_data["user"] = config["your_profile"]["name"]

            chat_data["chat_history"].append(message_data)

        # chat = Chat()
        # chat.chat(chat_data)

    def save_message_to_db(self, message: dict) -> None:
        """
        Save the message in the database.
        """
        try:
            person = Person.objects.get(pk=message["person"])
        except Person.DoesNotExist:
            person_data = self.tinderapi.get_profile(message["person"])

            photos = person_data["photos"]
            person_data.pop("photos", None)
            person = Person(**person_data)
            person.liked = True
            person.save()

            for photo_data in photos:
                photo = Photo(**photo_data, person=person)
                photo.save()

        message["person"] = person

        try:
            message = Message.objects.get(pk=message["id"])
        except Message.DoesNotExist:
            message = Message(**message)
            message.save()
