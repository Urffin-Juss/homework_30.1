from django.urls import path, include
from rest_framework import routers
from .views import CourseViewSet, LessonListCreatedView, LessonRetrieveUpdatedView, SubscribeView, UnsubscribeView

app_name = 'courses'

router = routers.DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreatedView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdatedView.as_view(), name='lesson-detail'),

    path("courses/<int:course_id>/subscribe/", SubscribeView.as_view(), name="course-subscribe"),
    path("courses/<int:course_id>/unsubscribe/", UnsubscribeView.as_view(), name="course-unsubscribe"),
    path("courses/<int:pk>/pay/", CreateCheckoutSessionView.as_view(), name="course-pay"),

]