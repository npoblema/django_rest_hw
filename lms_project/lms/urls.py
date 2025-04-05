from django.urls import path
from .views import LessonListView, LessonDetailView, SubscribeToCourseView, UnsubscribeFromCourseView, CourseListView

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/<int:pk>/subscribe/', SubscribeToCourseView.as_view(), name='subscribe'),
    path('courses/<int:pk>/unsubscribe/', UnsubscribeFromCourseView.as_view(), name='unsubscribe'),
    path('courses/', CourseListView.as_view(), name='course-list'),
]