from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habit.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        # Создание пользователя и его авторизация
        self.user = get_user_model().objects.create(email='user@example.com', password='password')
        self.other_user = get_user_model().objects.create(email='other@example.com', password='other_password')
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.old_habit = Habit.objects.create(
            user=self.user,
            action='brushing my teeth',
            time='22:30',
            place='bathroom',
            is_learned=True
        )

        self.new_habit = Habit.objects.create(
            user=self.user,
            action='going to bed before midnight',
            time='23:00',
            place='bedroom',
            related_habit=self.old_habit,
            is_public=True
        )

    def test_create_habit(self):
        """Тестирование создания привычки"""
        habit_data = {
            'action': 'rolling up a mat for yoga class',
            'time': '16:00',
            'place': 'at home',
            'reward': 'a glass of juice'
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что в ответе присутствует созданный урок
        self.assertEqual(response.data['action'], habit_data['action'])
        self.assertEqual(response.data['time'], '16:00:00')
        self.assertEqual(response.data['place'], habit_data['place'])
        self.assertEqual(response.data['reward'], habit_data['reward'])

    def test_list_habit(self):
        """ Вывод списка привычек """
        response = self.client.get(reverse('habit:habit-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        habits = [habit['action'] for habit in response.data['results']]
        self.assertIn('brushing my teeth', habits)
        self.assertIn('going to bed before midnight', habits)

    def test_public_list_habit(self):
        """ Вывод списка публичных привычек """
        response = self.client.get(reverse('habit:public-habit-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка наличия ключа 'results' в ответе
        self.assertIn('results', response.data)

        # Проверка длины списка результатов
        if response.data['results']:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data['results']), 0)

    def test_read_habit(self):
        """Тестирование просмотра привычки"""
        response = self.client.get(reverse('habit:habit', kwargs={'pk': self.new_habit.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'going to bed before midnight')

    def test_update_habit(self):
        """Тестирование редактирования привычки"""
        self.client.force_authenticate(user=self.user)
        habit_data = {
            'is_public': False
        }

        response = self.client.patch(reverse('habit:habit-update', kwargs={'pk': self.new_habit.pk}), data=habit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_public'], habit_data['is_public'])

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('habit:habit-delete', kwargs={'pk': self.new_habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(id=self.new_habit.id)

    # Тестирование валидаторов

    def test_invalid_reward_or_related_habit(self):
        """Тестирование отсутствия у новой привычки и вознаграждения, и связанной привычки"""

        habit_data = {
            'action': 'reading a book',
            'time': '23:00',
            'place': 'in bed',
            'reward': 'a glass of juice',
            'related_habit': self.old_habit.pk
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn('You have to add either a related habit or a reward.', response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_invalid_related_habit(self):
        """Тестирование, что новая привычка не может быть связанной привычкой"""

        habit_data = {
            'action': 'reading a book',
            'time': '22:40',
            'place': 'in bed',
            'related_habit': self.new_habit.pk
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn(f"Habit '{self.new_habit.action}' is not learned yet to become a related habit.",
                      response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_no_related_habit_or_reward(self):
        """Тестирование отсутствия связанной привычки или вознаграждения у выработанной привычки"""

        habit_data = {
            'action': 'rolling up a mat for yoga class',
            'time': '16:00',
            'place': 'at home',
            'is_learned': True,
            'reward': 'a glass of juice'
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn("Learned habit should have no related habits or rewards.", response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_invalid_time_sequence(self):
        """Тестирование, что новая привычка выполняется после связанной привычки"""

        habit_data = {
            'action': 'reading a book',
            'time': '22:00',
            'place': 'in bed',
            'related_habit': self.old_habit.pk
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn("New habit should be done after the related habit.",
                      response.content.decode())
        self.assertEqual(response.status_code, 400)

    # Тестирование разрешений

    def test_other_user_cannot_update_habit(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(reverse('habit:habit-update', kwargs={'pk': self.new_habit.pk}),
                                   data={'action': 'updated action'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_delete_habit(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('habit:habit-delete', kwargs={'pk': self.new_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
