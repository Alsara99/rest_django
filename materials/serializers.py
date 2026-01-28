from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lessons']

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        course = Course.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)
        return course
