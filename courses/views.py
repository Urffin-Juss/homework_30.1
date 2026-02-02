import stripe
from django.conf import settings
from django.contrib.messages.storage import session
from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginators import DefaultPagination
from .serializers import CourseSerializer, LessonSerializer
from courses.models import Course, Lesson, IsOwnerOrModerator, Subscription


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = DefaultPagination



class LessonListCreatedView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = DefaultPagination


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



class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout_Session.Create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "rub",
                    "product_data": {"name": course.title},
                    "unit_amount": int(course.price * 100),
                },
                "quantity": 1,
            }


        ],
        success_url = f"{settings.DOMAIN}/swagger/",
        cancel_url = f"{settings.DOMAIN}/swagger/",
        metadata = {
            "course_id": str(course.id),
            "user_id": str(request.user.id),
            }
        )


        return Response({'checkout_url': session.url}, status=status.HTTP_201_CREATED)















# Create your views here.
