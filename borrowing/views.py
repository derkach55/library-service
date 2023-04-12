import datetime

from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action in ("retrieve", "return_book"):
            return BorrowingRetrieveSerializer
        if self.action == 'create':
            return BorrowingCreateSerializer

        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        user_id = self.request.query_params.get('user_id', None)
        is_active = self.request.query_params.get('is_active', None)
        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user__id=user_id)
        if is_active == 'true':
            queryset = queryset.filter(actual_return__isnull=True)
        if is_active == 'false':
            queryset = queryset.filter(actual_return__isnull=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=True, permission_classes=[IsAdminUser],
            url_path='return', url_name='return_book')
    def return_book(self, request, pk=None):
        """Endpoint for returning book, if book is already returned, return appropriate message"""
        with transaction.atomic():
            borrowing = self.get_object()
            if not borrowing.actual_return:
                borrowing.book.inventory += 1
                borrowing.book.save()
                actual_return = datetime.date.today()
                serializer = self.get_serializer_class()(borrowing, data={'actual_return': actual_return}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({'actual_return': 'book has already returned'}, status=200)
