import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingRetrieveSerializer, BorrowingCreateSerializer

BORROWING_URL = reverse('borrowing:borrowing-list')


class TestUnauthenticatedBorrowingApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedBookApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()
        user = get_user_model().objects.create_user('test@test.com', 'test1234')
        admin = get_user_model().objects.create_user('admin@test.com', 'test1234', is_staff=True)
        self.client.force_authenticate(user)
        book = Book.objects.create(title='test', author='test', cover='SOFT', inventory=10, fee='1.00')
        self.borrowing = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=user
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=user,
            actual_return=datetime.date(2023, 5, 5)
        )
        self.borrowing3 = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=admin,
            actual_return=datetime.date(2023, 5, 5)
        )

    def test_list_borrowings(self):
        res = self.client.get(BORROWING_URL)
        serializer = BorrowingListSerializer(Borrowing.objects.filter(user_id=1), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(Borrowing.objects.filter(user_id=2), res.data)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_borrowings(self):
        res = self.client.get(reverse('borrowing:borrowing-detail', args=[1]))
        serializer = BorrowingRetrieveSerializer(Borrowing.objects.get(id=1))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_filter_borrowings(self):
        res = self.client.get(BORROWING_URL, {'is_active': 'true'})
        serializer = BorrowingListSerializer(
            Borrowing.objects.filter(user_id=1, actual_return__isnull=True), many=True
        )
        self.assertEqual(res.data, serializer.data)

        res2 = self.client.get(BORROWING_URL, {'is_active': 'false'})
        serializer2 = BorrowingListSerializer(
            Borrowing.objects.filter(user_id=1, actual_return__isnull=False), many=True
        )
        self.assertEqual(res2.data, serializer2.data)

    def test_create_borrowing(self):
        data = {
            "expected_return": "2023-05-25",
            "book": 1
        }
        res = self.client.post(BORROWING_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(res.data[key], value)


class TestAdminBorrowingApi(APITestCase):
    def setUp(self) -> None:
        self.client = self.client_class()
        user = get_user_model().objects.create_user('test@test.com', 'test1234')
        admin = get_user_model().objects.create_user('admin@test.com', 'test1234', is_staff=True)
        self.client.force_authenticate(admin)
        book = Book.objects.create(title='test', author='test', cover='SOFT', inventory=10, fee='1.00')
        self.borrowing = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=user
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=user,
            actual_return=datetime.date(2023, 5, 5)
        )
        self.borrowing3 = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=admin,
            actual_return=datetime.date(2023, 5, 5)
        )
        self.borrowing4 = Borrowing.objects.create(
            borrow_date=datetime.date.today(),
            expected_return=datetime.date(2023, 5, 5),
            book=book,
            user=admin
        )

    def test_filter_borrowings(self):
        res = self.client.get(BORROWING_URL)
        serializer = BorrowingListSerializer(Borrowing.objects.all(), many=True)
        self.assertEqual(res.data, serializer.data)
        res2 = self.client.get(BORROWING_URL, {'user_id': 1})
        serializer2 = BorrowingListSerializer(Borrowing.objects.filter(user_id=1), many=True)
        self.assertEqual(res2.data, serializer2.data)
        res3 = self.client.get(BORROWING_URL, {'user_id': 2})
        serializer3 = BorrowingListSerializer(Borrowing.objects.filter(user_id=2), many=True)
        self.assertEqual(res3.data, serializer3.data)

    def test_return_borrowing(self):
        res = self.client.get(reverse('borrowing:borrowing-return_book', args=[1]))
        serializer = BorrowingRetrieveSerializer(Borrowing.objects.get(id=1))
        self.assertEqual(serializer.data, res.data)
        self.assertEqual(Borrowing.objects.get(id=1).actual_return, datetime.date.today())
