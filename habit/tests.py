from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habit.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        # User creation and authorization
        self.user = get_user_model().objects.create(email='user@example.com', password='password')
        self.other_user = get_user_model().objects.create(email='other@example.com', password='other_password')
        self.client.force_authenticate(user=self.user)

        # Creation test habits
        self.old_habit = Habit.objects.create(
            user=self.user,
            action='brushing my teeth',
            time='22:30',
            place='bathroom',
            is_pleasant=True
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
        """ Testing habit creation """
        habit_data = {
            'action': 'rolling up a mat for yoga class',
            'time': '16:00',
            'place': 'at home',
            'reward': 'a glass of juice'
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the created lesson is present in the response
        self.assertEqual(response.data['action'], habit_data['action'])
        self.assertEqual(response.data['time'], '16:00:00')
        self.assertEqual(response.data['place'], habit_data['place'])
        self.assertEqual(response.data['reward'], habit_data['reward'])

    def test_list_habit(self):
        """ Testing the list of habits output """
        response = self.client.get(reverse('habit:habit-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        habits = [habit['action'] for habit in response.data['results']]
        self.assertIn('brushing my teeth', habits)
        self.assertIn('going to bed before midnight', habits)

    def test_public_list_habit(self):
        """ Testing the list of habits public output """
        response = self.client.get(reverse('habit:public-habit-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the 'results' key is present in the response
        self.assertIn('results', response.data)

        # Checking the length of the result list
        if response.data['results']:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data['results']), 0)

    def test_read_habit(self):
        """ Habit viewing test """
        response = self.client.get(reverse('habit:habit', kwargs={'pk': self.new_habit.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'going to bed before midnight')

    def test_update_habit(self):
        """ Habit editing test """
        self.client.force_authenticate(user=self.user)
        habit_data = {
            'is_public': False
        }

        response = self.client.patch(reverse('habit:habit-update', kwargs={'pk': self.new_habit.pk}), data=habit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_public'], habit_data['is_public'])

    def test_delete_habit(self):
        """ Habit deletion test """
        self.client.force_authenticate(user=self.user)
        url = reverse('habit:habit-delete', kwargs={'pk': self.new_habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(id=self.new_habit.id)

    # Validators testing

    def test_invalid_reward_or_related_habit(self):
        """ Testing the new habit's lack of both reward and bound habit """

        habit_data = {
            'action': 'reading a book',
            'time': '23:00',
            'place': 'in bed',
            'reward': 'a glass of juice',
            'related_habit': self.old_habit.pk
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn('You may add either a related habit or a reward.', response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_invalid_related_habit(self):
        """ Testing that a new habit can't be a related habit """

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
        """ Testing the absence of a related habit or reward in a learned habit """

        habit_data = {
            'action': 'rolling up a mat for yoga class',
            'time': '16:00',
            'place': 'at home',
            'is_pleasant': True,
            'reward': 'a glass of juice'
        }

        response = self.client.post(reverse('habit:habit-list-create'), data=habit_data)

        self.assertIn("Learned habit should have no related habits or rewards.", response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_no_related_habit_or_reward_on_update(self):
        """ Testing the absence of both a related habit and reward on updating the habit """
        self.client.force_authenticate(user=self.user)

        habit_data = {
            'reward': 'a glass of juice'
        }

        response = self.client.patch(reverse('habit:habit-update', kwargs={'pk': self.new_habit.pk}), data=habit_data)

        self.assertIn("You may add either a related habit or a reward.", response.content.decode())
        self.assertEqual(response.status_code, 400)

    def test_invalid_time_sequence(self):
        """ Testing that the new habit is performed after the related habit """

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

    # Permissions testing

    def test_other_user_cannot_update_habit(self):
        """ Testing that the user can't edit someone else's habits """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(reverse('habit:habit-update', kwargs={'pk': self.new_habit.pk}),
                                     data={'action': 'updated action'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_delete_habit(self):
        """ Testing that the user can't delete someone else's habits """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('habit:habit-delete', kwargs={'pk': self.new_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
