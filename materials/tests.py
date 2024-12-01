from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="sky", description="Очень хороший курс")
        self.lesson = Lesson.objects.create(name="DRF", description="Очень хороший урок", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "ООП"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "ООП"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "ООП"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertGreater(len(response.data), 0)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="sky", description="Очень хороший курс", owner=self.user)
        self.lesson = Lesson.objects.create(name="DRF", description="Очень хороший урок", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "name": "Sky"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Яндекс"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Яндекс"
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertGreater(len(response.data), 0)


class SubscriptionViewTests(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(email="admin@sky.pro")

        # Создаем тестовый курс
        self.course = Course.objects.create(name="sky", description="Очень хороший курс", owner=self.user)

    def test_subscribe_to_course(self):
        """ Тестирование добавления подписки на курс """
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        url = reverse('materials:subscribe')  # Убедитесь, что это правильный URL для вашего представления
        response = self.client.post(url, {'course_id': self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка добавлена")
        # Проверяем, что подписка была создана
        self.assertTrue(Subscription.objects.filter(owner=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """ Тестирование удаления подписки с курса """
        # Сначала добавим подписку
        Subscription.objects.create(owner=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        url = reverse('materials:subscribe')  # Убедитесь, что это правильный URL для вашего представления
        response = self.client.post(url, {'course_id': self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")
        self.assertFalse(Subscription.objects.filter(owner=self.user,
                                                     course=self.course).exists())  # Проверяем, что подписка была удалена

    def test_subscribe_to_nonexistent_course(self):
        """ Тестирование добавления подписки на несуществующий курс """
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        url = reverse('materials:subscribe')  # Убедитесь, что это правильный URL для вашего представления
        response = self.client.post(url, {'course_id': 999})  # Используем несуществующий ID курса

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user(self):
        """ Тестирование доступа неаутентифицированного пользователя """
        url = reverse('materials:subscribe')  # Убедитесь, что это правильный URL для вашего представления
        response = self.client.post(url, {'course_id': self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
