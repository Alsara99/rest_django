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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('way', 'course', 'lesson')
    ordering_fields = ('date',)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


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
