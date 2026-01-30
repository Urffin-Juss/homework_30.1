from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from courses.models import Course, Lesson, Subscription


User = get_user_model()


class CourseLessonApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u1@test.com", password="12345678", username="u1")
        self.course = Course.objects.create(title="C1", description="desc")
        self.lesson = Lesson.objects.create(course=self.course, title="L1", description="ok", preview=None, video_url="https://youtube.com/watch?v=123")

    def test_courses_list(self):
        r = self.client.get("/api/courses/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_lessons_crud(self):
        # create
        payload = {"course": self.course.id, "title": "L2", "description": "ok", "video_url": "https://youtube.com/watch?v=999"}
        r = self.client.post("/api/lessons/", payload, format="json")
        self.assertIn(r.status_code, (status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST))

        # retrieve
        r = self.client.get(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_validator_rejects_non_youtube(self):
        payload = {"course": self.course.id, "title": "BAD", "description": "ok", "video_url": "https://google.com/video"}
        r = self.client.post("/api/lessons/", payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_unsubscribe(self):
        self.client.force_authenticate(user=self.user)

        r = self.client.post(f"/api/courses/{self.course.id}/subscribe/")
        self.assertIn(r.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        r = self.client.delete(f"/api/courses/{self.course.id}/unsubscribe/")
        self.assertIn(r.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())