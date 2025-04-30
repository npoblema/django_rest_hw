from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription, Course
from users.models import User

@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course).select_related('user')
    subject = f'Обновление курса: {course.title}'
    message = f'Уважаемый пользователь,\n\nКурс "{course.title}" был обновлён. Проверьте новые материалы!\n\nС уважением,\nКоманда LMS'
    from_email = settings.EMAIL_HOST_USER or 'noreply@example.com'
    recipient_list = [sub.user.email for sub in subscribers if sub.user.email]

    if recipient_list:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

@shared_task
def block_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Blocked {count} inactive users"