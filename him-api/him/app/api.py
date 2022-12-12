from __future__ import annotations

import requests
from him.app.serializers import (
    MatchAPISerializer,
    PersonAPISerializer,
    MessageAPISerializer,
)

import json
import datetime

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

    def get_new_matches(self) -> Generator:
        """
        Get a list of new matches (i.e. 0 messages)
        """
        matches = self.__process_matches(message=0)

        for match in matches:
            yield match["id"], match["person"]["_id"], match["person"]["name"]

    def get_matches(self) -> Generator:
        """
        Get a list of matches (i.e. 1 messages).
        """
        matches = self.__process_matches(message=1)

        for match in matches:
            serializer = MatchAPISerializer(data=match)
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
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "X-Auth-Token": self.token
        }

        url = "https://api.gotinder.com" + url

        if method == "GET":
            r = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            r = requests.post(url, headers=headers, params=params, data=data)

        r.raise_for_status()

        if r.status_code == 204:
            return None

        return r.json()



class BumbleAPIClient:
    def __init__(self, cookie):
        self.cookie = cookie


    def like(self, user_id):
        """
        Like a profile.
        """

        ping_back = "5c67acc00d1f1f8a157bb855bce1c1db"

        url = "SERVER_ENCOUNTERS_VOTE"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 80,
                    "server_encounters_vote": {
                        "person_id": user_id,
                        "vote": 2,
                        "vote_source": 1,
                        "game_mode": 0,
                    },
                }
            ],
            "message_id": 1,
            "message_type": 80,
            "version": 1,
            "is_background": False,
        }

        res = self.__request("POST", url, data, ping_back=ping_back)

        print(res)

    def dislike(self, user_id):
        """
        Dislike a profile.
        message_id += 2
        """
        message_id = 19

        url = "SERVER_ENCOUNTERS_VOTE"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 80,
                    "server_encounters_vote": {
                        "person_id": user_id,
                        "vote": 3,
                        "vote_source": 1,
                        "game_mode": 0,
                    },
                }
            ],
            "message_id": 26,
            "message_type": 80,
            "version": 1,
            "is_background": False,
        }

        self.__request("POST", url, data)

    def get_encounters(self):
        """
        Pagination is with last person_id:

            {"$gpb":"badoo.bma.BadooMessage","body":[{"message_type":81,"server_get_encounters":{"number":10,"context":1,"user_field_filter":{"projection":[210,370,200,230,490,540,530,560,291,732,890,930,662,570,380,493,1140,1150,1160,1161],"request_albums":[{"album_type":7},{"album_type":12,"external_provider":12,"count":8}],"game_mode":0,"request_music_services":{"top_artists_limit":8,"supported_services":[29],"preview_image_size":{"width":120,"height":120}}},"last_person_id":"zAgEACTUwMzg3MDA1MgggvshqAAAAACCELS1y6UaxAV-EHI082uxFnmXeko2NwOYrNCWljo_iCQ"}}],"message_id":23,"message_type":81,"version":1,"is_background":false}
        """
        ping_back = "31bc026378e43d9573cfd24338161c8f"

        url = "SERVER_GET_ENCOUNTERS"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 81,
                    "server_get_encounters": {
                        "number": 10,
                        "context": 1,
                        "user_field_filter": {
                            "projection": [
                                210,
                                370,
                                200,
                                230,
                                490,
                                540,
                                530,
                                560,
                                291,
                                732,
                                890,
                                930,
                                662,
                                570,
                                380,
                                493,
                                1140,
                                1150,
                                1160,
                                1161,
                            ],
                            "request_albums": [
                                {"album_type": 7},
                                {
                                    "album_type": 12,
                                    "external_provider": 12,
                                    "count": 8,
                                },
                            ],
                            "game_mode": 0,
                            "request_music_services": {
                                "top_artists_limit": 8,
                                "supported_services": [29],
                                "preview_image_size": {"width": 120, "height": 120},
                            },
                        },
                    },
                },
            ],
            "message_id": 7,
            "message_type": 81,
            "version": 1,
            "is_background": False,
        }

        res = self.__request("POST", url, data, ping_back)

        data = []

        for result in res["body"][0]["client_encounters"]["results"]:
            user = {
                "id": result["user"]["user_id"],
                "name": result["user"]["name"],
                "age": result["user"]["age"],
                "gender": result["user"]["gender"],
            }

            for field in result["user"]["profile_fields"]:
                if field["id"] == "location":
                    user["city"] = field["display_value"]
                if field["id"] == "aboutme_text":
                    user["bio"] = field["display_value"]

            data.append(user)

        return data

    def get_matches(self):

        ping_back = "d211c8f15ee93247b0341ac8651be3c6"

        url = "SERVER_GET_USER_LIST"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 245,
                    "server_get_user_list": {
                        "user_field_filter": {
                            "projection": [
                                200,
                                210,
                                340,
                                230,
                                640,
                                580,
                                300,
                                860,
                                280,
                                590,
                                591,
                                250,
                                700,
                                762,
                                592,
                                880,
                                582,
                                930,
                                585,
                                583,
                                305,
                                330,
                                763,
                                1423,
                                584,
                                1262,
                                911,
                                912,
                            ]
                        },
                        "preferred_count": 30,
                        "folder_id": 0,
                    },
                }
            ],
            "message_id": 5,
            "message_type": 245,
            "version": 1,
            "is_background": False,
        }

        res = self.__request("POST", url, data, ping_back=ping_back)

        users = res["body"][0]["client_user_list"]["section"][1]["users"]

        results = []

        for user in users:
            person = {
                "id": user["user_id"],
                "name": user["name"],
                "birth_date": self.get_birthday(user["age"]),
            }

            results.append(person)

        return results

    def get_birthday(self, age: int):
        """
        Get the birthday in format Y-m-d from age.
        Ex: 39 -> 1983-01-01
        Ex: 18 -> 2004-01-01
        """
        today = datetime.datetime.today()
        return today.replace(year=today.year - age).strftime("%Y-%m-%d")



    def get_chat_message(self, chat_instance_id):
        url = "SERVER_OPEN_CHAT"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 102,
                    "server_open_chat": {
                        "user_field_filter": {
                            "projection": [
                                200,
                                210,
                                340,
                                230,
                                640,
                                580,
                                300,
                                860,
                                280,
                                590,
                                591,
                                250,
                                700,
                                762,
                                592,
                                880,
                                582,
                                930,
                                585,
                                583,
                                305,
                                330,
                                763,
                                1423,
                                584,
                                1262,
                                911,
                                912,
                            ],
                            "request_albums": [
                                {
                                    "count": 10,
                                    "offset": 1,
                                    "album_type": 2,
                                    "photo_request": {
                                        "return_preview_url": True,
                                        "return_large_url": True,
                                    },
                                }
                            ],
                        },
                        "chat_instance_id": chat_instance_id,
                        "message_count": 50,
                    },
                }
            ],
            "message_id": 6,
            "message_type": 102,
            "version": 1,
            "is_background": False,
        }

        self.__request("POST", url, data)

    def __request(self, method, url, data, ping_back=None):
        """
        NOTE: ping back must be set
        """
        data = json.dumps(data, separators=(",", ":"))

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Content-Type": "application/json",
            "X-Pingback": ping_back,
            "x-use-session-cookie": "1",
            "Cookie": self.cookie,
        }

        url = "https://am1.bumble.com/mwebapi.phtml?" + url

        response = requests.request(
            method, url, headers=headers, data=data
        )
        results = response.json()

        if results["message_type"] in (1, 124):
            raise Exception(results)

        return results