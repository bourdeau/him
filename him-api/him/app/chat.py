from string import Template

from him.app.ai import Him
from him.settings import config
from him.app.helpers import Base


class Chat(Base):
    """
    Chat with a Profile.
    """

    def __init__(self) -> None:
        super().__init__()

    def chat(self, chat_data: list) -> None:
        """
        Chat with a Match.
        """
        chat = Him(api_key=config["openai_secret"])

        her_id_match = chat_data["her"]["id_match"]
        her_bio = chat_data["her"].get("bio")
        her_name = chat_data["her"]["name"]

        shorten_chat_history = chat_data["chat_history"][-30:]

        self.logger.info(f"💬 Chating with {her_name}")

        # Check if the last message is from you
        if shorten_chat_history[-1]["user"] == config["your_profile"]["name"]:
            self.logger.info("❌ You wrote the last message")
            return

        # Check if the profile is in the white list
        if self.__is_in_white_list(her_id_match):
            self.logger.info("❌ She is in your whitelist")
            return

        # Create the context template for OpenAI
        context = Template(config["chat"]["context"]).substitute(
            your_profile_name=config["your_profile"]["name"],
            your_profile_bio=config["your_profile"]["bio"],
            her_name=her_name,
            her_bio=her_bio,
        )

        message_data = chat.talk(context=context, chat_history=shorten_chat_history)

        # Send the message
        self.tinderapi.send_message(her_id_match, message_data["message"])

        self.logger.info("✏️ You sent her this message: %s", message_data["message"])

    def __is_in_white_list(self, her_id: str) -> bool:
        """
        Check if the profile is in the white list.
        """
        for white in config["white_list"]:
            if her_id == white["id"]:
                return True

        return False
