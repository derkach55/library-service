from rest_framework import viewsets, mixins

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingRetrieveSerializer
from book.permissions import IsAdminOrReadOnly


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
