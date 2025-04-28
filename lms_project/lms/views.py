# lms/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, PaymentSerializer
from .services import create_stripe_checkout_session

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Получение списка курсов", responses={200: CourseSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Создание курса", responses={201: CourseSerializer, 403: None})
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Только администраторы могут создавать курсы'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(summary="Получение списка курсов", responses={200: CourseSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Создание урока", responses={201: LessonSerializer, 403: None})
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Только администраторы могут создавать уроки'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Подписка на курс", responses={201: SubscriptionSerializer, 400: None})
    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
            if created:
                return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
            return Response({'message': 'Вы уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary="Отписка от курса", responses={204: None, 404: None})
    def delete(self, request, pk):
        subscription = Subscription.objects.filter(user=request.user, course_id=pk)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)

class PaymentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Создание платежа", responses={201: {'payment_url': 'string'}, 404: None})
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
    @extend_schema(summary="Успешная оплата", responses={200: None})
    def get(self, request):
        return Response({'message': 'Оплата успешно завершена'}, status=status.HTTP_200_OK)

class PaymentCancelView(APIView):
    @extend_schema(summary="Отмена оплаты", responses={200: None})
    def get(self, request):
        return Response({'message': 'Оплата отменена'}, status=status.HTTP_200_OK)