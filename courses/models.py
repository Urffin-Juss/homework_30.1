from django.db import models
from django.conf import settings



class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='courses/%Y/%m', blank=True, null=True)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses'
    )


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

    video_url = models.URLField(verbose_name='video url', null=True, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_lessons'
    )


    class Meta:
        db_table = 'lesson'
        ordering = ['title']

    def __str__(self):
        return self.title


class IsOwnerOrModerator(models.Model):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return obj.owwner == request.user

