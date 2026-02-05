from .apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

from materials.views import CourseViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet)


urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/retrieve', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription'),
] + router.urls
