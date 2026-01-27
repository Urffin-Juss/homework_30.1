from rest_framework import serializers
from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course


class LessonSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(source='lesson_count', True, read_only=True)

    class Meta:
        model = Lesson
