from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class LessonAndSubscriptionTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@test.com',
            password='12345'
        )
        self.other_user = User.objects.create_user(
            email='user@test.com',
            password='12345'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='12345',
            is_staff=True
        )

        self.course = Course.objects.create(
            name='Test Course',
            description='Test description',
            owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Lesson description',
            course=self.course,
            owner=self.owner
        )


    def test_lesson_list_authenticated_user(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get('/materials/lessons/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_lesson_create_owner(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            "name": "New Lesson",
            "description": "New description",
            "course": self.course.id
        }

        response = self.client.post('/materials/lessons/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_not_owner_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            "name": "New Lesson",
            "description": "New description",
            "course": self.course.id
        }

        response = self.client.post('/materials/lessons/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f'/materials/lessons/{self.lesson.id}/',
            {"name": "Updated Lesson"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete_owner(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(
            f'/materials/lessons/{self.lesson.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_delete_not_owner_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(
            f'/materials/lessons/{self.lesson.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_subscribe_course(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            '/materials/subscriptions/',
            {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.other_user,
                course=self.course
            ).exists()
        )

    def test_unsubscribe_course(self):
        Subscription.objects.create(
            user=self.other_user,
            course=self.course
        )

        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            '/materials/subscriptions/',
            {"course_id": self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.other_user,
                course=self.course
            ).exists()
        )

    def test_course_subscription_flag(self):
        Subscription.objects.create(
            user=self.other_user,
            course=self.course
        )

        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(
            f'/materials/courses/{self.course.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_subscribed'))
