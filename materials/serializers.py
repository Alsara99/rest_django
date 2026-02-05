from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import YouTubeOnlyValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'description',
            'preview',
            'video_link',
            'course'
        ]
        validators = [
            YouTubeOnlyValidator(field='video_url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'preview',
            'video_url',
            'lessons',
            'lesson_count',
            'is_subscribed',
        ]
        validators = [
            YouTubeOnlyValidator(field='video_url')
        ]

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()
