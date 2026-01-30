from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CourseSerializer, LessonSerializer
from courses.models import Course, Lesson, IsOwnerOrModerator, Subscription


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


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id: int):
        course = Course.objects.get(pk=course_id)
        Subscription.objects.get_or_create(user=request.user, course=course)
        return Response({"detail": "subscribed"}, status=status.HTTP_201_CREATED)


class UnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id: int):
        Subscription.objects.filter(user=request.user, course_id=course_id).delete()
        return Response({"detail": "unsubscribed"}, status=status.HTTP_204_NO_CONTENT)















# Create your views here.
