from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import CourseSerializer, LessonSerializer
from courses.models import Course, Lesson, IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]



class LessonListCreatedView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonRetrieveUpdatedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]















# Create your views here.
