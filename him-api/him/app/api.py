import requests
from him.app.serializers import (
    MatchAPISerializer,
    PersonAPISerializer,
    MessageAPISerializer,
)
from typing import Generator
from him.settings import config


class TinderAPIClient:
    """
    Tinder API Client.
    """

    def __init__(self, token) -> None:
        self.token = token

    def like(self, user_id: str) -> None:
        """
        Like a user.
        """
        self.__request("POST", f"/like/{user_id}")

    def dislike(self, user_id: str) -> None:
        """
        Dislike a user.
        """
        self.__request("POST", f"/pass/{user_id}")

    def get_likables(self) -> Generator:
        """
        Get a list of users that you can like.
        """
        res = self.__request("GET", "/recs/core")

        if not res or not "results" in res:
            return

        for result in res["results"]:
            serializer = PersonAPISerializer(data=result)
            serializer.is_valid(raise_exception=True)

            yield serializer

    def get_new_matches(self) -> list:
        """
        Get a list of new matches (i.e. 0 messages)
        """
        matches = self.__process_matches(message=0)

        for match in matches:
            yield match["id"], match["person"]["_id"], match["person"]["name"]

    def get_matches(self):
        """
        Get a list of matches (i.e. 1 messages).
        """
        matches = self.__process_matches(message=1)

        for result in matches:
            serializer = MatchAPISerializer(data=result)
            serializer.is_valid(raise_exception=True)

            yield serializer

    def __process_matches(self, message: int) -> list:
        """
        Process matches.
        """
        params = {
            "count": 60,
            "message": message,
            "is_tinder_u": False,
        }

        matches = []
        next_page_token = None

        while True:
            if next_page_token:
                params["page_token"] = next_page_token

            res = self.__request("GET", "/v2/matches", params=params)
            next_page_token = res["data"].get("next_page_token")

            if not res:
                break

            matches = matches + res["data"]["matches"]

            if not next_page_token:
                break

        return matches

    def get_messages(self, match_id: str) -> list:
        """
        Get messages from a match.
        """
        parmas = {
            "count": 100,
        }

        url = f"/v2/matches/{match_id}/messages"

        res = self.__request("GET", url=url, params=parmas)

        messages = res["data"]["messages"]
        messages.reverse()

        results = []

        for result in messages:
            result["sent_from"] = result["from"]
            result["sent_to"] = result["to"]
            del result["from"]
            del result["to"]

            serializer = MessageAPISerializer(data=result)
            serializer.is_valid(raise_exception=True)

            results.append(serializer)

        return results

    def send_message(self, match_id: str, other_id: str, message: str) -> None:
        """
        Send a message to a match
        """
        url = f"/user/matches/{match_id}"

        params = {
            "locale": "fr",
        }
        data = {
            "userId": config["your_profile"]["id"],
            "otherId": other_id,
            "matchId": match_id,
            "message": message,
        }

        self.__request("POST", url=url, params=params, data=data)

    def get_profile(self, profile_id: str) -> dict:
        res = self.__request("GET", f"/user/{profile_id}")

        if not res:
            return

        serializer = PersonAPISerializer(data=res["results"])
        serializer.is_valid(raise_exception=True)

        return serializer

    def __request(self, method, url, headers=None, params=None, data=None):
        """
        Make a request to the Tinder API
        """
        headers = {"X-Auth-Token": self.token}

        url = "https://api.gotinder.com" + url

        if method == "GET":
            r = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            r = requests.post(url, headers=headers, params=params, data=data)

        r.raise_for_status()

        if r.status_code == 204:
            return None

        return r.json()
