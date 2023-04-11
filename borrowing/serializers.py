from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('id', 'expected_return', 'actual_return', 'borrow_date', 'book', 'user')
        read_only_fields = ('id', 'user', 'actual_return', 'borrow_date')


class BorrowingListSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
