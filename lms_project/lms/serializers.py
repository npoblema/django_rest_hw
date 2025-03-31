from rest_framework import serializers
from .models import Lesson, Course, Subscription
from .validators import validate_no_external_links

class LessonSerializer(serializers.ModelSerializer):
    content = serializers.CharField(validators=[validate_no_external_links])

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'course', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False