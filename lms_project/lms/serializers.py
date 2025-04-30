from rest_framework import serializers
from .models import Course, Lesson, Payment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'owner', 'last_updated']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'course', 'owner']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'payment_date', 'payment_intent_id']
        read_only_fields = ['user', 'payment_date', 'payment_intent_id']