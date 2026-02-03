from django.db import models
from django.conf import settings



class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='courses/%Y/%m', blank=True, null=True)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses'
    )


    class Meta:
        db_table = 'course'
        ordering = ['title']

    def save(self, *args, **kwargs):
        # При создании или изменении цены обновляем в Stripe
        creating = not self.pk
        old_price = None

        if not creating:
            try:
                old_instance = Course.objects.get(pk=self.pk)
                old_price = old_instance.price
            except Course.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Обновляем в Stripe при изменении цены
        if not creating and old_price != self.price:
            self.update_strip_price()


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



class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возврат'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    stripe_session_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='RUB')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"Payment {self.id} - {self.user.email} - {self.amount} {self.currency}"
