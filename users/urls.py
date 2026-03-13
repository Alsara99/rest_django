from .apps import UsersConfig
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet


app_name = UsersConfig.name

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('payments', PaymentViewSet)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
] + router.urls
