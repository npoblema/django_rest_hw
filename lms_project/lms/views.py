from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Lesson, Course, Subscription, Payment
from .serializers import LessonSerializer, CourseSerializer
from .paginators import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from .services import create_stripe_checkout_session

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

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    @extend_schema(
        description="Получение списка всех уроков.",
        parameters=[
            OpenApiParameter(name='course_id', type=int, description='ID курса для фильтрации уроков'),
        ],
        responses={200: LessonSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Создание нового урока. Доступно только администраторам.",
        request=LessonSerializer,
        responses={201: LessonSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class PaymentCreateView(APIView):
    def post(self, request):
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                amount=course.price
            )
            stripe_data = create_stripe_checkout_session(payment)
            payment.stripe_session_id = stripe_data['session_id']
            payment.payment_url = stripe_data['payment_url']
            payment.save()
            return Response({'payment_url': payment.payment_url}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentSuccessView(APIView):
    def get(self, request):
        return Response({'message': 'Оплата успешно завершена'}, status=status.HTTP_200_OK)

class PaymentCancelView(APIView):
    def get(self, request):
        return Response({'message': 'Оплата отменена'}, status=status.HTTP_200_OK)