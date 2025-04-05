from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Lesson, Course, Subscription
from .serializers import LessonSerializer, CourseSerializer
from .paginators import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class CourseListView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Можно переопределить PAGE_SIZE здесь
        page = paginator.paginate_queryset(courses, request)
        serializer = CourseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class LessonListView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class SubscribeToCourseView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def post(self, request, pk):
        course = self.get_object()
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if created:
            return Response({"message": "Подписка оформлена"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Вы уже подписаны"}, status=status.HTTP_200_OK)

class UnsubscribeFromCourseView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def delete(self, request, pk):
        course = self.get_object()
        deleted, _ = Subscription.objects.filter(user=request.user, course=course).delete()
        if deleted:
            return Response({"message": "Подписка отменена"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Подписка не найдена"}, status=status.HTTP_404_NOT_FOUND)