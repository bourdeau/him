import random
from string import Template

from him.settings import config


class MessageTemplate:
    """
    Chat with a Profile.
    """

    def get_message(self, profile_name) -> str:
        """
        Get message from template
        """
        msg_template = random.choice(config["chat"]["first_messages"])
        message = Template(msg_template).substitute(name=profile_name)

        return message
