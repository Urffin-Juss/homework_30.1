from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Course, Subscription




@shared_task
def notify_course_updates(course_id: int)
    course = Course.objects.get(pk=course_id)

    subs = Subscription.objects.filter(course=course).select_related("user")
    emails = [s.user.email for s in subs if s.user.email]

    if not emails:
        return 0

    subject = f"Course updates for {course.title}"
    message = f"In course {course.title} we have new update. Check your lms for more information"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )

    course.last_notification_at = timezone.now()
    course.save(update_fields=["last_notification_at"])
    return len(emails)


