# lms/serializers.py
from rest_framework import serializers
from .models import Course, Lesson, Subscription, Payment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'owner']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'course', 'owner']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'payment_url', 'status']