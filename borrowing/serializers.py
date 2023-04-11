import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('id', 'expected_return', 'actual_return', 'borrow_date', 'book', 'user')
        read_only_fields = ('id', 'user', 'actual_return', 'borrow_date')

    def validate(self, attrs):
        borrow_date = attrs.get('borrow_date', datetime.date.today())
        if attrs['expected_return'] < borrow_date:
            raise ValidationError('Expected return date should be after the borrow date.')
        actual_return = attrs.get('actual_return', None)
        if actual_return and borrow_date > actual_return:
            raise ValidationError('Actual return date should be after the borrow date.')
        return attrs


class BorrowingListSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(read_only=True)
