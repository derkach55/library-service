from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

BOOK_URL = reverse('book:book-list')


class TestUnauthenticatedBookApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, 200)
        res2 = self.client.post(BOOK_URL)
        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedBookApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()
        user = get_user_model().objects.create_user('test@test.com', 'test1234')
        self.client.force_authenticate(user)

    def test_create_book_forbidden(self):
        data = {
            'title': 'title',
            'author': 'author',
            'cover': 'HARD',
            'inventory': 10,
            'fee': '1.00'
        }
        res = self.client.post(BOOK_URL, data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestAdminBookApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()
        user = get_user_model().objects.create_user(
            'test@test.com', 'test1234', is_staff=True
        )
        self.client.force_authenticate(user)

    def test_create_book(self):
        data = {
            'title': 'title',
            'author': 'author',
            'cover': 'HARD',
            'inventory': 10,
            'fee': '1.00'
        }
        res = self.client.post(BOOK_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(res.data[key], value)
