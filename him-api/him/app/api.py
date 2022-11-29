import requests
from datetime import datetime
from him.app.serializers import PersonAPISerializer
from typing import Generator

class TinderAPI:
    """
    TODO: please use Serializer and stop pissing rubbish code...
    """

    def __init__(self, token) -> None:
        self.token = token

    def get_likables(self) -> Generator:
        """
        Get a list of users that you can like
        """
        res = self.__request("GET", "/recs/core")

        if not res:
            return

        for result in res["results"]:            
            serializer = PersonAPISerializer(data=result)
            serializer.is_valid(raise_exception=True)
            
            yield serializer


    def like(self, user_id: str) -> None:
        """
        Like a user
        """
        self.__request("POST", f"/like/{user_id}")

    def dislike(self, user_id: str) -> None:
        """
        Dislike a user
        """
        self.__request("POST", f"/pass/{user_id}")

    def get_new_matches(self) -> list:
        """
        Get a list of new matches
        """
        params = {
            "count": 60,
            "message": 1,
            "is_tinder_u": False,
        }

        res = self.__request("GET", "/v2/matches", params=params)

        matches = res["data"]["matches"]

        data = []

        for match in matches:
            user = {
                "id": match["_id"],
                "name": match["person"]["name"],
                "bio": match["person"].get("bio"),
            }
            data.append(user)

        return data

    def get_matches(self) -> list:
        """
        Get a list of matches
        TODO: count must be the exact number of matches
        """
        params = {
            "count": 60,
            "message": 1,
            "is_tinder_u": False,
        }

        res = self.__request("GET", "/v2/matches", params=params)

        if not res:
            return

        matches = res["data"]["matches"]

        data = []

        for match in matches:
            birth_date = None

            if match["person"].get("birth_date"):
                birth_date = datetime.strptime(
                    match["person"]["birth_date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                birth_date = birth_date.date()

            user = {
                "id_match": match["_id"],
                "id_profile": match["person"]["_id"],
                "name": match["person"]["name"],
                "bio": match["person"].get("bio"),
                "birth_date": birth_date,
            }
            data.append(user)

        return data

    def get_messages(self, match_id: str) -> list:
        """
        Get messages from a match
        """
        parmas = {
            "count": 100,
        }

        url = f"/v2/matches/{match_id}/messages"

        res = self.__request("GET", url=url, params=parmas)

        messages = res["data"]["messages"]

        results = []

        for message in messages:
            message = {
                "id": message["_id"],
                "person": message["from"],
                "message": message["message"],
                "sent_date": message["sent_date"],
            }
            results.append(message)

        return results

    def send_message(self, match_id: str, message: str) -> None:
        """
        Send a message to a match
        """
        url = f"/user/matches/{match_id}"

        data = {"message": message}

        self.__request("POST", url, data=data)

    def get_profile(self, profile_id: str):
        res = self.__request("GET", f"/user/{profile_id}")

        if not res:
            return

        results = res["results"]

        birth_date = None

        if results.get("birth_date"):
            birth_date = datetime.strptime(
                results["birth_date"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            birth_date = birth_date.date()

        user = {
            "id": results["_id"],
            "name": results["name"],
            "bio": results["bio"],
            "gender": results["gender"],
            "distance_mi": results["distance_mi"],
            "birth_date": birth_date,
            "photos": [],
        }

        for photo in results["photos"]:
            photo_data = {
                "id": photo["id"],
                "url": photo["url"],
                "score": photo.get("score"),
            }
            user["photos"].append(photo_data)

        return user

    def get_updates(self):
        """
        Get updates from the Tinder API
        """
        url = f"/updates"

        params = {
            "locale": "fr",
        }

        data = {"last_activity_date": "2022-11-29T06:06:28.132Z"}

        res = self.__request("POST", url=url, params=params, data=data)

        return res

    def __request(self, method, url, headers=None, params=None, data=None):
        """
        Make a request to the Tinder API
        """
        headers = {
            "Accept": "application/json",
            "X-Auth-Token": self.token,
            "Accept-Language": "fr,fr-FR,en-US,en",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "tinder-version": "3.53.0",
        }

        url = "https://api.gotinder.com" + url

        if method == "GET":
            r = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            r = requests.post(url, headers=headers, params=params, data=data)

        if r.status_code == 204:
            return None

        r.raise_for_status()

        return r.json()