import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('id', 'expected_return', 'actual_return', 'borrow_date', 'book', 'user')


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('id', 'expected_return', 'book')

    def validate(self, attrs):
        borrow_date = attrs.get('borrow_date', datetime.date.today())
        if attrs['expected_return'] < borrow_date:
            raise ValidationError('Expected return date should be after the borrow date.')
        actual_return = attrs.get('actual_return', None)
        if actual_return and borrow_date > actual_return:
            raise ValidationError('Actual return date should be after the borrow date.')
        if attrs['book'].inventory < 1:
            raise ValidationError({'Book_inventory': 'Book inventory must be greater 0'})
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['book'].inventory -= 1
            validated_data['book'].save()
            return super(BorrowingCreateSerializer, self).create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(read_only=True)
