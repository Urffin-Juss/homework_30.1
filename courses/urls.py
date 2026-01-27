from django.urls import path, include
from rest_framework import routers
from .models import Course, Lesson
from .views import CourseViewSet

app_name = 'courses'

router = routers.DefaultRouter()

router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),


]