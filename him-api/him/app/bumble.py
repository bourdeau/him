import hashlib
import requests
import json
import datetime

"""
TODO: In progress...
"""
class BumbleAPIClient:
    def __init__(self, cookie):
        self.cookie = cookie
        self.salt = "whitetelevisionbulbelectionroofhorseflying"


    def like(self, user_id):
        """
        Like a profile.
        """
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
            "message_type": 80,
            "version": 1,
        }

        return self.__request("POST", url, data)

    def dislike(self, user_id):
        """
        Dislike a profile.
        message_id += 2
        """
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
            "message_type": 80,
            "version": 1,
        }

        self.__request("POST", url, data)

    def get_encounters(self):
        """
        Get Encounters.
        """
        url = "SERVER_GET_ENCOUNTERS"

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "server_get_encounters": {
                        "number": 20,
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
                        },
                    },
                },
            ],
            "message_type": 81,
            "version": 1
        }

        res = self.__request("POST", url, data)

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

        res = self.__request("POST", url, data)

        users = res["body"][0]["client_user_list"]["section"][1]["users"]

        results = []

        for user in users:
            person = {
                "id": user["user_id"],
                "name": user["name"],
                "birth_date": self.__get_birthday(user["age"]),
                "is_locked": user["is_locked"]
            }

            results.append(person)

        return results

    def __get_birthday(self, age: int):
        """
        Get the birthday in format Y-m-d from age.
        Ex: 39 -> 1983-01-01
        Ex: 18 -> 2004-01-01
        """
        today = datetime.datetime.today()

        return today.replace(year=today.year - age).strftime("%Y-%m-%d")

    def get_chat_message(self, user_id):
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
                        "chat_instance_id": user_id,
                        "message_count": 50,
                    },
                }
            ],
            "message_id": 6,
            "message_type": 102,
            "version": 1,
            "is_background": False,
        }

        res =  self.__request("POST", url, data)

        messages = res["body"][0]["client_open_chat"]["chat_messages"]

        results = []

        for message in messages:
            chat = {
                "from_person_id": message["from_person_id"],
                "to_person_id": message["to_person_id"],
                "mssg": message["mssg"],
                "date_created": message["date_created"]

            }

            results.append(chat)

        return results

    def send_message(self, user_id, message):
        url = "SERVER_SEND_CHAT_MESSAGE"

        uuid = int(datetime.datetime.now().timestamp()*1000)

        data = {
            "$gpb": "badoo.bma.BadooMessage",
            "body": [
                {
                    "message_type": 104,
                    "chat_message": {
                        "mssg": message,
                        "message_type": 1,
                        "uid": uuid,
                        "from_person_id": "zAhMACjE3OTE1NDA3NjgAINxseyIKUZ8pwOoADSILJq9nGzFVPLRHCwoxvX0LzSSH",
                        "to_person_id": user_id,
                        "read": False,
                    },
                }
            ],
            "message_id": 24,
            "message_type": 104,
            "version": 1,
            "is_background": False,
        }

        res = self.__request("POST", url, data)

        return res

    def __generate__x_pingback(self, body_json):
        str2hash = body_json + self.salt
        result = hashlib.md5(str2hash.encode())
        
        return result.hexdigest()


    def __request(self, method, url, data):
        data = json.dumps(data, separators=(",", ":"))

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Content-Type": "application/json",
            "X-Pingback": self.__generate__x_pingback(data),
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


if __name__ == "__main__":
    cookie = 'session_cookie_name=session; device_id=0fcee216-e216-16aa-fzzf3-f34669b45a3a; buzz_lang_code=en-us; first_web_visit_id=11980bdd3f38924887b16c349904b0f43f456443; last_referred_web_visit_id=042bfe004866ff6f28d84e52838731fc03a06be2; dnsDisplayed=undefined; ccpaApplies=false; signedLspa=undefined; ccpaUUID=52c88717-3061-450d-8d19-5b2fab45fdac; consentUUID=360556ad-318f-4265-96b2-1544e4a3f6b4_14; aid=1791540768; cpc=%7B%22c%22%3A0%2C%22e%22%3A1673018036522%2C%22u%22%3A%22zAhMACjE3OTE1NDA3NjgAINxseyIKUZ8pwOoADSILJq9nGzFVPLRHCwoxvX0LzSSH%22%7D; _sp_su=false; HDR-X-User-id=zAhMACjE3OTE1NDA3NjgAINxseyIKUZ8pwOoADSILJq9nGzFVPLRHCwoxvX0LzSSH; cookie_banner_closed=true; session=s4:221:Z2sXI7pErCz4hrqhosEABll8POlllN253UzPMoPy'
    client = BumbleAPIClient(cookie=cookie)

    persons = client.get_encounters()

    for person in persons:
        client.like(person["id"])

    # matches = client.get_matches()

    # for match in matches:

    #     if not match["is_locked"]:
    #         messages = client.get_chat_message(match["id"])
    #         print(messages)


    # message = "Mais j'imagine que tu as du trouver une relation sérieuse depuis le temps"
    # res = client.send_message("zAhMACTYzMDMzODgzNgggvshqAAAAACB0pVc3NA1ylJgJZY-JJ7F_ieMA9VQqFwgFeVNFxizCJA", message)

    # print(res)