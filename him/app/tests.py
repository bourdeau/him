from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):
    fixtures = ["personn"]

    def test(self):
        self.assertEqual(1, 1)
