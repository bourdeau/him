import random
from string import Template
from him.app.models import MessageTemplate as MessageTemplateModel


class MessageTemplate:
    """
    Chat with a Profile.
    """

    def get_message(self, profile_name) -> str:
        """
        Get message from template
        """
        templates = MessageTemplateModel.objects.all()

        msg_tpl = random.choice(templates)
        msg_tpl.nb_sent += 1
        msg_tpl.save()

        message = Template(msg_tpl.message).substitute(name=profile_name)

        return message
