from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingRetrieveSerializer


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
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id', None)
        is_active = self.request.query_params.get('is_active', None)
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if is_active == 'true':
            queryset = queryset.filter(actual_return__isnull=True)
        if is_active == 'false':
            queryset = queryset.filter(actual_return__isnull=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
