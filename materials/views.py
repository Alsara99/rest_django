from django.core.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permission import IsOwnerOrModerator, IsNotModerator
from .paginators import CoursePagination, LessonPagination
from.tasks import send_course_update_email


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Удалять может только владелец")
        instance.delete()


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()

        subscriptions = Subscription.objects.filter(course=course)
        emails = [
            sub.user.email
            for sub in subscriptions
            if sub.user.email
        ]

        if emails:
            send_course_update_email.delay(emails, course.title)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course = get_object_or_404(Course, id=course_id)

        subs_qs = Subscription.objects.filter(
            user=user,
            course=course
        )

        # Если подписка есть — удаляем
        if subs_qs.exists():
            subs_qs.delete()
            message = 'подписка удалена'
        # Если подписки нет — создаём
        else:
            Subscription.objects.create(
                user=user,
                course=course
            )
            message = 'подписка добавлена'

        return Response({"message": message})
