from .models import Payment, User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    PaymentSerializer,
)
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # если платим за курс
        if payment.course:
            course = payment.course

            product_id = create_stripe_product(course)
            price_id = create_stripe_price(product_id, payment.amount)
            session_url = create_checkout_session(price_id)

            payment.stripe_product_id = product_id
            payment.stripe_price_id = price_id
            payment.stripe_session_url = session_url
            payment.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
