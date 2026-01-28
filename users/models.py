from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields  import PhoneNumberField
from django.conf import settings



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)




class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30, null=True, verbose_name='username')
    email = models.EmailField(unique=True, max_length=254, null=True, verbose_name='email address')
    first_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='first name')
    last_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='last name')
    phone_number = PhoneNumberField(max_length=11)
    city = models.CharField(max_length=255,)
    avatar = models.ImageField(upload_to='avatars/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



    def __str__(self):
        return self.email




class Payment(models.Model):
    """Payment model"""

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'cash'),
        ('transfer', 'transfer'),

    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='user',
    )
    payment_date = models.DateField(verbose_name='payment date')
    paid_course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='paid course',
    )

    paid_lesson = models.ForeignKey(
        'lessons.Lesson',
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

    def __str__(self):
        return f"Payment {self.id} from {self.user.email} - {self.amount}"

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ('-payment_date',)



