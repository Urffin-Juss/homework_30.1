from django.db import models
from django.conf import settings



class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='courses/%Y/%m', blank=True, null=True)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
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
        related_name='courses'
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



class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"

    def __str__(self):
        return f"{self.user_id} -> {self.course_id}"
