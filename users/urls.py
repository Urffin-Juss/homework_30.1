from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses.views import CourseViewSet
from .views import PaymentViewSet, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = router.urls



