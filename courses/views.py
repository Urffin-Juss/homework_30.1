from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework import generics
from .serializers import CourseSerializer, LessonSerializer

from courses.models import Course, Lesson



class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]



class LessonListCreatedView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonRetrieveUpdatedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]












# Create your views here.
