# lms/models.py
from django.db import models
from django.conf import settings
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'  # добавляем уникальное имя для обратной связи
    )


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='lessons'  # добавляем для связи с курсом
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons'  # добавляем уникальное имя для обратной связи
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма в рублях
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    payment_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, succeeded, failed

    def __str__(self):
        return f"Платеж {self.user.email} за {self.course.title}"