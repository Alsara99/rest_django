from .apps import UsersConfig
from django.urls import path
from .views import *

app_name = UsersConfig.name


urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]