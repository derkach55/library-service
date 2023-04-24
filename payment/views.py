from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related('borrowing')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(borrowing__user=self.request.user)

        return queryset

    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny],
            url_path='success', url_name='success')
    def payment_success(self, request):
        """Success Payment view, mark payment as paid"""
        session = request.query_params.get('session_id')
        payment = Payment.objects.get(session_id=session)
        serializer = self.get_serializer_class()(payment, data={'status': 'PAID'}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
