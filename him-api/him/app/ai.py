from __future__ import annotations

import openai

from him.settings import config


class Him:
    """
    Chat with a Profile.
    """

    def __init__(self, api_key: str) -> None:
        """
        Args:
            api_key (str): The OpenAI API key.
        """
        openai.api_key = api_key
        self.completion = openai.Completion()
        self.your_name = config["your_profile"]["name"]

    def talk(self, context: str, chat_history: list[dict]) -> list[dict]:
        """
        Return new messages based on a context and a chat history.
        """
        prompt = context + "\n\n"

        for item in chat_history:
            prompt += f"{item['user']}: {item['message']}\n"

        prompt += f"{self.your_name}:"

        response = self.__ask(prompt)

        return self.__format_response(response)

    def __ask(self, prompt: str) -> str:
        """
        Request completion to OpenAI
        """
        response = self.completion.create(
            prompt=prompt,
            engine="text-davinci-002",
            stop=f"\n{self.your_name}",
            temperature=0.9,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.8,
            best_of=1,
            max_tokens=1500,
        )

        return response.choices[0].text.strip()

    def __format_response(self, response) -> list:
        """
        Fromat the response a dict
        """
        response = f"{self.your_name}: {response}"
        responses = response.splitlines()
        line = responses[0]
        line_list = line.split(f"{self.your_name}: ")

        return {"user": self.your_name, "message": line_list[1].lstrip()}
