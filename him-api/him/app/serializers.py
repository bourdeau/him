from rest_framework import serializers
from him.app.models import Person, Photo


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


# API Serializers
class PhotoAPISerializer(serializers.Serializer):

    id = serializers.CharField()
    url = serializers.CharField()
    score = serializers.FloatField(required=False)


class PersonAPISerializer(serializers.Serializer):

    _id = serializers.CharField(source="id")
    name = serializers.CharField()
    bio = serializers.CharField(
        required=False,
        max_length=None,
        min_length=None,
        allow_blank=True,
        trim_whitespace=True,
    )
    birth_date = serializers.DateTimeField(
        required=False, input_formats=["iso-8601"], format="Y-m-d"
    )
    distance_mi = serializers.IntegerField(required=False)
    gender = serializers.IntegerField()
    photos = PhotoAPISerializer(required=False, many=True)

    def create(self, validated_data):
        photos_data = validated_data.pop("photos")

        person = Person(**validated_data)
        person.save()

        for photo_data in photos_data:
            photo = Photo(**photo_data)
            photo.person = person
            photo.save()
            person.photo_set.add(photo)

        return person


class MessageAPISerializer(serializers.Serializer):

    _id = serializers.CharField(source="id")
    person = serializers.CharField()
    message = serializers.CharField()
    sent_date = serializers.DateTimeField()


test = {
    "seen": {"match_seen": True},
    "_id": "62d7d7a14e95f00100f1cc1963743f4dff70120100911568",
    "id": "62d7d7a14e95f00100f1cc1963743f4dff70120100911568",
    "closed": False,
    "common_friend_count": 0,
    "common_like_count": 0,
    "created_date": "2022-11-28T20:19:29.670Z",
    "dead": False,
    "last_activity_date": "2022-11-28T20:19:29.670Z",
    "message_count": 0,
    "messages": [],
    "participants": ["63743f4dff70120100911568"],
    "pending": False,
    "is_super_like": False,
    "is_boost_match": False,
    "is_super_boost_match": False,
    "is_primetime_boost_match": False,
    "is_experiences_match": False,
    "is_fast_match": False,
    "is_preferences_match": False,
    "is_matchmaker_match": False,
    "is_opener": True,
    "has_shown_initial_interest": False,
    "person": {
        "_id": "63743f4dff70120100911568",
        "badges": [{"type": "selfie_verified"}],
        "bio": "Passionné de voyages 🌏 29📍\nKz-Ru-Fra-Eng\n",
        "birth_date": "1983-12-02T13:05:12.672Z",
        "gender": 1,
        "name": "Raushka",
        "ping_time": "2014-12-09T00:00:00.000Z",
        "photos": [
            {
                "id": "a2068e73-a278-4e16-9d2a-123d76cc8544",
                "crop_info": {
                    "user": {
                        "width_pct": 1.0,
                        "x_offset_pct": 0.0,
                        "height_pct": 0.8,
                        "y_offset_pct": 0.0,
                    },
                    "algo": {
                        "width_pct": 0.2137414320837706,
                        "x_offset_pct": 0.31129100827965883,
                        "height_pct": 0.2739073354005814,
                        "y_offset_pct": 0.12606406490318478,
                    },
                    "processed_by_bullseye": True,
                    "user_customized": False,
                    "faces": [
                        {
                            "algo": {
                                "width_pct": 0.2137414320837706,
                                "x_offset_pct": 0.31129100827965883,
                                "height_pct": 0.21975148836150768,
                                "y_offset_pct": 0.18021991194225848,
                            },
                            "bounding_box_percentage": 4.7,
                        },
                        {
                            "algo": {
                                "width_pct": 0.03688538302667438,
                                "x_offset_pct": 0.42172606899403037,
                                "height_pct": 0.03543332421220838,
                                "y_offset_pct": 0.12606406490318478,
                            },
                            "bounding_box_percentage": 0.13,
                        },
                    ],
                },
                "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/original_a2068e73-a278-4e16-9d2a-123d76cc8544.jpeg",
                "processedFiles": [
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/640x800_a2068e73-a278-4e16-9d2a-123d76cc8544.jpg",
                        "height": 800,
                        "width": 640,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/320x400_a2068e73-a278-4e16-9d2a-123d76cc8544.jpg",
                        "height": 400,
                        "width": 320,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/172x216_a2068e73-a278-4e16-9d2a-123d76cc8544.jpg",
                        "height": 216,
                        "width": 172,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/84x106_a2068e73-a278-4e16-9d2a-123d76cc8544.jpg",
                        "height": 106,
                        "width": 84,
                    },
                ],
                "fileName": "a2068e73-a278-4e16-9d2a-123d76cc8544.jpg",
                "extension": "jpg,webp",
                "webp_qf": [75],
                "rank": 0,
                "score": 0.43148562,
                "win_count": 3,
                "type": "image",
                "assets": [],
                "media_type": "image",
            },
            {
                "id": "c40b3767-7a74-4de8-9f19-b4eb4e676cda",
                "crop_info": {
                    "user": {
                        "width_pct": 1.0,
                        "x_offset_pct": 0.0,
                        "height_pct": 0.8,
                        "y_offset_pct": 0.0,
                    },
                    "algo": {
                        "width_pct": 0.05234090811572967,
                        "x_offset_pct": 0.5267439271789044,
                        "height_pct": 0.06565196797717361,
                        "y_offset_pct": 0.11418880462180823,
                    },
                    "processed_by_bullseye": True,
                    "user_customized": False,
                    "faces": [
                        {
                            "algo": {
                                "width_pct": 0.05234090811572967,
                                "x_offset_pct": 0.5267439271789044,
                                "height_pct": 0.06565196797717361,
                                "y_offset_pct": 0.11418880462180823,
                            },
                            "bounding_box_percentage": 0.34,
                        }
                    ],
                },
                "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/original_c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpeg",
                "processedFiles": [
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/640x800_c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpg",
                        "height": 800,
                        "width": 640,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/320x400_c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpg",
                        "height": 400,
                        "width": 320,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/172x216_c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpg",
                        "height": 216,
                        "width": 172,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/84x106_c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpg",
                        "height": 106,
                        "width": 84,
                    },
                ],
                "fileName": "c40b3767-7a74-4de8-9f19-b4eb4e676cda.jpg",
                "extension": "jpg,webp",
                "webp_qf": [75],
                "rank": 1,
                "score": 0.31314498,
                "win_count": 2,
                "type": "image",
                "assets": [],
                "media_type": "image",
            },
            {
                "id": "f73a9ce5-6e1b-4870-b7ec-6092ae172bb3",
                "crop_info": {
                    "user": {
                        "width_pct": 1.0,
                        "x_offset_pct": 0.0,
                        "height_pct": 0.8,
                        "y_offset_pct": 0.0,
                    },
                    "algo": {
                        "width_pct": 0.4109831053530797,
                        "x_offset_pct": 0.3407800035784021,
                        "height_pct": 0.440337706618011,
                        "y_offset_pct": 0.011016241461038589,
                    },
                    "processed_by_bullseye": True,
                    "user_customized": False,
                    "faces": [
                        {
                            "algo": {
                                "width_pct": 0.4109831053530797,
                                "x_offset_pct": 0.3407800035784021,
                                "height_pct": 0.440337706618011,
                                "y_offset_pct": 0.011016241461038589,
                            },
                            "bounding_box_percentage": 18.1,
                        }
                    ],
                },
                "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/original_f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpeg",
                "processedFiles": [
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/640x800_f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpg",
                        "height": 800,
                        "width": 640,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/320x400_f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpg",
                        "height": 400,
                        "width": 320,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/172x216_f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpg",
                        "height": 216,
                        "width": 172,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/84x106_f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpg",
                        "height": 106,
                        "width": 84,
                    },
                ],
                "fileName": "f73a9ce5-6e1b-4870-b7ec-6092ae172bb3.jpg",
                "extension": "jpg,webp",
                "webp_qf": [75],
                "rank": 2,
                "score": 0.16633256,
                "win_count": 1,
                "type": "image",
                "assets": [],
                "media_type": "image",
            },
            {
                "id": "8d58ed18-b42f-4411-a583-dc8385cba91f",
                "crop_info": {
                    "user": {
                        "width_pct": 1.0,
                        "x_offset_pct": 0.0,
                        "height_pct": 0.8,
                        "y_offset_pct": 0.12140804431401192,
                    },
                    "algo": {
                        "width_pct": 0.8953721846221014,
                        "x_offset_pct": 0.07350355032831431,
                        "height_pct": 0.5248453020490706,
                        "y_offset_pct": 0.2589853932894766,
                    },
                    "processed_by_bullseye": True,
                    "user_customized": False,
                    "faces": [
                        {
                            "algo": {
                                "width_pct": 0.43131221495568756,
                                "x_offset_pct": 0.07350355032831431,
                                "height_pct": 0.46776853217743336,
                                "y_offset_pct": 0.2589853932894766,
                            },
                            "bounding_box_percentage": 20.18,
                        },
                        {
                            "algo": {
                                "width_pct": 0.4316901509882882,
                                "x_offset_pct": 0.5371855839621276,
                                "height_pct": 0.4569856920558959,
                                "y_offset_pct": 0.3268450032826513,
                            },
                            "bounding_box_percentage": 19.73,
                        },
                    ],
                },
                "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/original_8d58ed18-b42f-4411-a583-dc8385cba91f.jpeg",
                "processedFiles": [
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/640x800_8d58ed18-b42f-4411-a583-dc8385cba91f.jpg",
                        "height": 800,
                        "width": 640,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/320x400_8d58ed18-b42f-4411-a583-dc8385cba91f.jpg",
                        "height": 400,
                        "width": 320,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/172x216_8d58ed18-b42f-4411-a583-dc8385cba91f.jpg",
                        "height": 216,
                        "width": 172,
                    },
                    {
                        "url": "https://images-ssl.gotinder.com/63743f4dff70120100911568/84x106_8d58ed18-b42f-4411-a583-dc8385cba91f.jpg",
                        "height": 106,
                        "width": 84,
                    },
                ],
                "fileName": "8d58ed18-b42f-4411-a583-dc8385cba91f.jpg",
                "extension": "jpg,webp",
                "webp_qf": [75],
                "rank": 3,
                "score": 0.08903684,
                "win_count": 0,
                "type": "image",
                "assets": [],
                "media_type": "image",
            },
        ],
    },
    "following": True,
    "following_moments": True,
    "readreceipt": {"enabled": False},
    "subscription_tier": "platinum",
    "is_archived": False,
}
