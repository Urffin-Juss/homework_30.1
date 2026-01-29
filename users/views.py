from django.shortcuts import renderfrom rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['paid_date',]
    ordering = ('-paid_date',)






# Create your views here.
