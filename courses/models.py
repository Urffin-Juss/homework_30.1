from django.core.exceptions import ValidationError
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
    last_notification_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"

    def __str__(self):
        return f"{self.user_id} -> {self.course_id}"



class Payment(models.Model):
    """Payment model"""

    id = models.UUIDField(primary_key=True,  editable=False)

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'cash'),
        ('transfer', 'transfer'),

    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='user',
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name='payment date')
    paid_course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='paid course',
    )

    paid_lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='paid lesson',

    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='amount',
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='payment method',
    )



    def clean(self):
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError("Укажите paid_course или paid_lesson.")

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ('-payment_date',)

    def __str__(self):
        return f"{self.user.email} - {self.amount}"



