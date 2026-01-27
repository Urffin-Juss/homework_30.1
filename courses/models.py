from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='courses/%Y/%m', blank=True, null=True)
    description = models.TextField(max_length=500)
    description = models.TextField(max_length=500)


    class Meta:
        db_table = 'course'
        ordering = ['title']


    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course,
        on_delete=models.CASCADE,
        related_name='lessons', )
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='lessons/%Y/%m')
    description = models.TextField(max_length=500)


    class Meta:
        db_table = 'lesson'
        ordering = ['title']

    def __str__(self):
        return self.title


# Create your models here.
