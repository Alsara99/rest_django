from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lessons', 'lesson_count']

    def get_lesson_count(self, obj):
        if obj.lesson_set.exists():
            return obj.lesson_set.count()
        else:
            return 0
