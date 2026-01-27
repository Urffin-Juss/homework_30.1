from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='courses/%Y/%m')
    description = models.TextField(max_length=500)


    class Meta:
        db_table = 'course'
        ordering = ['title']


class Lesson(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='lessons/%Y/%m')
    description = models.TextField(max_length=500)


    class Meta:
        db_table = 'lesson'
        ordering = ['title']


# Create your models here.
