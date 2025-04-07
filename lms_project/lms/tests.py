# lms/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Course, Lesson, Subscription

class LessonCRUDTest(APITestCase):
    def setUp(self):
        # Убираем username, используем только email
        self.user = User.objects.create_user(email='testuser@example.com', password='123456')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='admin123')
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            video_url='https://youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

    def test_create_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('lesson-list-create')
        data = {
            'title': 'New Lesson',
            'video_url': 'https://youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_with_forbidden_link(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list-create')
        data = {
            'title': 'Invalid Lesson',
            'video_url': 'https://example.com/video',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_lesson_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SubscriptionTest(APITestCase):
    def setUp(self):
        # Убираем username, используем только email
        self.user = User.objects.create_user(email='testuser@example.com', password='123456')
        self.course = Course.objects.create(title='Test Course', owner=self.user)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('subscribe', kwargs={'pk': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('subscribe', kwargs={'pk': self.course.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())