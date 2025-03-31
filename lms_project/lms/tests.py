from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from lms.models import Lesson, Course, Subscription
from rest_framework import status

class LessonCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.course = Course.objects.create(title='Test Course', owner=self.admin)
        self.lesson = Lesson.objects.create(
            title='Test Lesson', content='Lesson content', course=self.course, owner=self.admin
        )

    def test_create_lesson_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'New Lesson', 'content': 'Content with youtube.com link', 'course': self.course.id}
        response = self.client.post('/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_with_forbidden_link(self):
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'New Lesson', 'content': 'Content with http://example.com', 'course': self.course.id}
        response = self.client.post('/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_lesson_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_as_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Lesson', 'content': 'Updated content'}
        response = self.client.put(f'/lessons/{self.lesson.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SubscriptionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.course = Course.objects.create(title='Test Course', owner=self.user)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/courses/{self.course.id}/unsubscribe/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())