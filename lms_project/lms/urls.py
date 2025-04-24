# lms/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, PaymentCreateView, PaymentSuccessView, PaymentCancelView, SubscribeView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = router.urls + [
    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('subscribe/<int:pk>/', SubscribeView.as_view(), name='subscribe'),
]