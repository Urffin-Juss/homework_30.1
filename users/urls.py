from django.urls import path, include
from rest_framework import routers

from courses.views import CourseViewSet
from models import Payment

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', basename='users')
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('users', Payment.as_view(), name='payment'),]