from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):
    fixtures = ["person"]

    def test(self):
        self.assertEqual(1, 1)
