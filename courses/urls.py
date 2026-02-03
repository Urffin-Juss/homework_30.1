from django.urls import path, include
from rest_framework import routers
from .models import Course, Lesson
from .views import CourseViewSet, LessonListCreatedView, LessonRetrieveUpdatedView

app_name = 'courses'

router = routers.DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreatedView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdatedView.as_view(), name='lesson-detail'),


]