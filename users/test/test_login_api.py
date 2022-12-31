# File created at 2022-03-08 06:26:17 UTC
from authentication.api.views import LoginView
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.test.factories import UserFactory


class TestLoginAPI(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(username='testuser', password='Test@123')
        self.endpoint = settings.API_PREFIX + 'auth/login/'


    def test_login_api(self):
        request = self.factory.post(self.endpoint, {
            'username': 'testuser',
            'password': 'Test@123'
        })
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.user.token)
        self.assertEqual(response.data['username'], self.user.username)


    def test_login_api_invalid_credentials(self):
        request = self.factory.post(self.endpoint, {
            'username': 'testuser',
            'password': 'Test@1234'
        })
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['errors']['error'][0].title().lower(),
            'A user with this username and password was not found.'.lower()
        )


    def test_if_inactive_user_cannot_login(self):
        user = UserFactory(username='testuser', password='Test@123')
        user.is_active = False
        user.save()

        request = self.factory.post(self.endpoint, {
            'username': 'testuser',
            'password': 'Test@123'
        })
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['errors']['error'][0].title().lower(),
            'User account has been deactivated.'.lower()
        )


    def test_login_required_fields(self):
        request = self.factory.post(self.endpoint, {})
        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['username'][0].code, 'required')
        self.assertEqual(response.data['errors']['password'][0].code, 'required')
