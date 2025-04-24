# lms/models.py
from django.db import models
from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    payment_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Платеж {self.user.email} за {self.course.title}"