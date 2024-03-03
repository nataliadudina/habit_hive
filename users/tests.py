from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        # self.user = get_user_model().objects.create(email='user@example.com')
        # self.user.set_password('password')
        # self.user.save()
        self.user = get_user_model().objects.create(email='user@example.com', password='password')

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.other_user = get_user_model().objects.create(email='other@example.com')
        self.other_user.set_password('other_password')
        self.other_user.save()

    def test_view_own_profile(self):
        """Тестирование просмотра собственного профиля"""
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['email'], self.user.email)
        self.assertTrue('habits' in response.data)
        self.assertTrue('last_name' in response.data)

    def test_view_other_profile(self):
        """Тестирование просмотра чужого профиля"""
        access_token = str(RefreshToken.for_user(self.other_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(reverse('users:profile', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе содержатся только ограниченные поля
        self.assertTrue('email' in response.data)
        self.assertTrue('country' in response.data)
        self.assertTrue('public_habits' in response.data)
        self.assertTrue('habits' not in response.data)

    def test_edit_own_profile(self):
        """Тестирование редактирования собственного профиля"""
        user_data = {
            'username': 'User'
        }
        response = self.client.patch(reverse('users:profile-put-patch', kwargs={'pk': self.user.pk}), data=user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user_data['username'])

    def test_edit_other_profile(self):
        """Тестирование редактирования чужого профиля"""
        user_data = {
            'username': 'User'
        }
        access_token = str(RefreshToken.for_user(self.other_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.patch(reverse('users:profile-put-patch', kwargs={'pk': self.user.pk}), data=user_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserRegistrationTest(APITestCase):

    def test_successful_registration(self):
        """Тестирование регистрации пользователя"""
        user_data = {
            'email': 'user@example.com',
            'password': 'password'
        }

        url = reverse('users:user-post')
        response = self.client.post(url, user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=user_data['email'])
        self.assertTrue(user.check_password(user_data['password']))
