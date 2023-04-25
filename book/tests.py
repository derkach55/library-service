from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from book.models import Book
from book.serializers import BookSerializer

BOOK_URL = reverse('book:book-list')


class TestUnauthenticatedBookApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()
        self.book1 = Book.objects.create(title='test', author='test', cover='SOFT', inventory=10, fee='1.00')
        self.book2 = Book.objects.create(title='test2', author='test2', cover='HARD', inventory=20, fee='2.00')

    def test_auth_required(self):
        res2 = self.client.post(BOOK_URL)
        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_book(self):
        res = self.client.get(BOOK_URL)
        serializer = BookSerializer(Book.objects.all(), many=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book(self):
        res = self.client.get(reverse('book:book-detail', args=[1]))
        serializer = BookSerializer(self.book1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)


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
