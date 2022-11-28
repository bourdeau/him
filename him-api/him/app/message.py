import random
from string import Template

from him.settings import config


class Message:
    """
    Chat with a Profile.
    """

    def get_message(self, profile_name) -> None:
        """
        Get message from template
        """
        msg_template = random.choice(config["chat"]["first_messages"])
        message = Template(msg_template).substitute(name=profile_name)

        return message
