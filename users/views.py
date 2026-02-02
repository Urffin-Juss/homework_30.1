from rest_framework import generics
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .models import User
from .serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = User.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter()

        return queryset






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
