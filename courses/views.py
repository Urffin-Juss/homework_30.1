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

    def get_queryset(self):
        qs = Course.objects.all().annotate(lessons_count=Count("lessons")).order_by("id")
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class LessonListCreatedView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Lesson.objects.all().order_by("id")
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdatedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Lesson.objects.all().order_by("id")
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)















# Create your views here.
