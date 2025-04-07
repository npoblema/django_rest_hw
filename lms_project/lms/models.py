# lms/models.py
from django.db import models
from django.conf import settings


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
