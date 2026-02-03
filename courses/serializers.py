from rest_framework import serializers
from courses.models import Course, Lesson, Subscription
from courses.validators import validate_only_youtube_url, validate_no_external_links_except_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(required=False, allow_null=True, validators=[validate_only_youtube_url])
    description = serializers.CharField(validators=[validate_no_external_links_except_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Course
        fields = '__all__'


    def get_lessons_count(self, obj):
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "user", "course", "created_at")
        read_only_fields = ("id", "created_at", "user")