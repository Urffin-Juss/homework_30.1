from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from rest_framework import generics
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .models import User
from .serializers import PaymentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        is_moderator = user.groups.filter(name="moderators").exists()
        if user.is_staff or user.is_superuser or is_moderator:
            return User.objects.all()
        return User.objects.filter(id=user.id)






class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['paid_date',]
    ordering = ('-paid_date',)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]




# Create your views here.
