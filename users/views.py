from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter


class PaymentRetrieveAPIView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['date']
    ordering_fields = ['course', 'lesson', 'way']
