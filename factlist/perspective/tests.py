from django.test import TestCase
from rest_framework import status

from factlist.users.tests import UserTestMixin


class PerspectiveTestCase(TestCase, UserTestMixin):

    def test_create_topic(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test topic")

    def test_get_list_of_topics(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/topics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        data = {
            'title': 'Test topic2',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/topics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_an_topic(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get("/api/v1/topics/%s/" % response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test topic")

    def test_update_an_topic(self):
        enis, enis_client = self.create_user_and_user_client()
        ali, ali_client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "title": "Test topic edit"
        }
        response = enis_client.patch('/api/v1/topics/%s/' % response.data["id"], data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "title": "Test topic edit"
        }
        response = ali_client.patch('/api/v1/topics/%s/' % response.data["id"], data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_topic(self):
        enis, enis_client = self.create_user_and_user_client()
        ali, ali_client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        topic_id = response.data["id"]

        response = ali_client.delete('/api/v1/topics/%s/' % topic_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = enis_client.delete('/api/v1/topics/%s/' % topic_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_a_link(self):
        enis, enis_client = self.create_user_and_user_client()

        data = {
            'title': 'Test topic',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/topics/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        topic_id = response.data["id"]

        data = {
            "link": "https://twitter.com"
        }
        response = enis_client.post("/api/v1/topics/%s/links/" % topic_id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
