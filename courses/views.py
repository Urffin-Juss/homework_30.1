from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

from courses.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()









# Create your views here.
