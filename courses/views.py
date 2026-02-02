import stripe
from django.conf import settings
from django.db.models import Count
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .paginators import DefaultPagination
from .serializers import CourseSerializer, LessonSerializer
from courses.models import Course, Lesson, IsOwnerOrModerator, Subscription


# ==================== COURSE VIEWSET ====================

@swagger_auto_schema(
    method='get',
    operation_description="Получить список всех курсов",
    responses={200: CourseSerializer(many=True)}
)
@swagger_auto_schema(
    method='post',
    operation_description="Создать новый курс",
    request_body=CourseSerializer,
    responses={
        201: CourseSerializer,
        400: "Неверные данные"
    }
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами.

    Предоставляет полный CRUD для курсов с проверкой прав доступа.
    """
    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = DefaultPagination


# ==================== LESSON VIEWS ====================

@swagger_auto_schema(
    method='get',
    operation_description="Получить список всех уроков",
    responses={200: LessonSerializer(many=True)}
)
@swagger_auto_schema(
    method='post',
    operation_description="Создать новый урок",
    request_body=LessonSerializer,
    responses={
        201: LessonSerializer,
        400: "Неверные данные"
    }
)
class LessonListCreatedView(generics.ListCreateAPIView):
    """
    Создание и получение списка уроков.

    Доступно всем пользователям без аутентификации.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = DefaultPagination


@swagger_auto_schema(
    method='get',
    operation_description="Получить информацию об уроке по ID",
    responses={
        200: LessonSerializer,
        404: "Урок не найден"
    }
)
@swagger_auto_schema(
    method='put',
    operation_description="Полностью обновить урок",
    request_body=LessonSerializer,
    responses={
        200: LessonSerializer,
        400: "Неверные данные",
        404: "Урок не найден"
    }
)
@swagger_auto_schema(
    method='patch',
    operation_description="Частично обновить урок",
    request_body=LessonSerializer,
    responses={
        200: LessonSerializer,
        400: "Неверные данные",
        404: "Урок не найден"
    }
)
@swagger_auto_schema(
    method='delete',
    operation_description="Удалить урок",
    responses={
        204: "Урок удален",
        404: "Урок не найден"
    }
)
class LessonRetrieveUpdatedView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление конкретного урока.

    Доступно всем пользователям без аутентификации.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


# ==================== SUBSCRIPTION VIEWS ====================

class SubscribeView(APIView):
    """
    Подписка на курс.

    Требуется аутентификация через JWT токен.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Подписаться на курс",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_PATH,
                description="ID курса для подписки",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                description="Подписка создана",
                examples={
                    "application/json": {
                        "detail": "subscribed"
                    }
                }
            ),
            404: openapi.Response(
                description="Курс не найден",
                examples={
                    "application/json": {
                        "detail": "Not found"
                    }
                }
            )
        }
    )
    def post(self, request, course_id: int):
        try:
            course = Course.objects.get(pk=course_id)
            Subscription.objects.get_or_create(user=request.user, course=course)
            return Response({"detail": "subscribed"}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class UnsubscribeView(APIView):
    """
    Отписка от курса.

    Требуется аутентификация через JWT токен.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Отписаться от курса",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_PATH,
                description="ID курса для отписки",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: openapi.Response(
                description="Отписка выполнена"
            ),
            404: openapi.Response(
                description="Подписка не найдена",
                examples={
                    "application/json": {
                        "detail": "Subscription not found"
                    }
                }
            )
        }
    )
    def delete(self, request, course_id: int):
        deleted, _ = Subscription.objects.filter(
            user=request.user,
            course_id=course_id
        ).delete()

        if deleted:
            return Response({"detail": "unsubscribed"}, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Subscription not found"},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== STRIPE PAYMENT VIEW ====================

class CreateCheckoutSessionView(APIView):
    """
    Создание платежной сессии Stripe для оплаты курса.

    Требуется аутентификация через JWT токен.
    Создает сессию оплаты в Stripe и возвращает URL для перехода.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать сессию оплаты курса через Stripe",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID курса для оплаты",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                description="Платежная сессия создана",
                examples={
                    "application/json": {
                        "checkout_url": "https://checkout.stripe.com/pay/cs_test_..."
                    }
                }
            ),
            400: openapi.Response(
                description="Ошибка Stripe или неверные данные",
                examples={
                    "application/json": {
                        "error": "Invalid Stripe API key"
                    }
                }
            ),
            404: openapi.Response(
                description="Курс не найден",
                examples={
                    "application/json": {
                        "error": "Course not found"
                    }
                }
            )
        }
    )
    def post(self, request, pk):
        try:
            # Получаем курс
            course = Course.objects.get(pk=pk)

            # Проверяем, что у курса есть цена
            if not course.price or course.price <= 0:
                return Response(
                    {"error": "Course price must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Настраиваем Stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Создаем сессию оплаты
            session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "rub",
                            "product_data": {
                                "name": course.title,
                                "description": course.description[:500] if course.description else "Курс"
                            },
                            "unit_amount": int(course.price * 100),  # в копейках
                        },
                        "quantity": 1,
                    }
                ],
                success_url=f"{settings.DOMAIN}/api/payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN}/api/payment/cancel/",
                metadata={
                    "course_id": str(course.id),
                    "user_id": str(request.user.id),
                    "course_title": course.title
                },
                customer_email=request.user.email if request.user.email else None,
            )

            return Response(
                {'checkout_url': session.url},
                status=status.HTTP_201_CREATED
            )

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )