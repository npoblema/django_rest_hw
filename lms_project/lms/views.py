from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from .tasks import send_course_update_email
from rest_framework_simplejwt.authentication import JWTAuthentication

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    @extend_schema(summary="Обновление курса", responses={200: CourseSerializer, 403: None})
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Только администраторы могут обновлять курсы'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.last_updated < timezone.now() - timedelta(hours=4):
            send_course_update_email.delay(instance.id)
        return Response(serializer.data)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    @extend_schema(summary="Обновление урока", responses={200: LessonSerializer, 403: None})
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Только администраторы могут обновлять уроки'}, status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.course.last_updated < timezone.now() - timedelta(hours=4):
            send_course_update_email.delay(instance.course.id)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)