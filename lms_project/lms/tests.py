# lms/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Course, Lesson, Subscription

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {'email': 'newuser@example.com', 'password': 'pass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_user(self):
        User.objects.create_user(email='testuser@example.com', password='pass123')
        url = reverse('token_obtain_pair')
        data = {'email': 'testuser@example.com', 'password': 'pass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class CourseTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@example.com', password='admin123')
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.course = Course.objects.create(title='Test Course', price=100.00, owner=self.user)

    def test_create_course_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('course-list')
        data = {'title': 'New Course', 'price': 200.00, 'description': ''}  # Добавлено description
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-list')
        data = {'title': 'New Course', 'price': 200.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LessonCRUDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='admin123')
        self.course = Course.objects.create(title='Test Course', price=100.00, owner=self.user)
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            video_url='https://youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

    def test_create_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('lesson-list')
        data = {
            'title': 'New Lesson',
            'video_url': 'https://youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_lesson_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345')
        self.course = Course.objects.create(title='Test Course', price=100.00, owner=self.user)

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