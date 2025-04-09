from django.urls import path
from .views import LessonViewSet, PaymentCreateView, PaymentSuccessView, PaymentCancelView

urlpatterns = [
    path('lessons/', LessonViewSet.as_view({'get': 'list', 'post': 'create'}), name='lesson-list-create'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]