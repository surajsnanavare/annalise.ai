from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.api.views import SignupAPIView
from users.test.factories import UserFactory


class TestUserSignupAPI(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.endpoint = settings.API_PREFIX + '/users/signup/'
        self.valid_payload = {
            'username': 'testuser',
            'password': 'test@123',
            'first_name': 'test',
            'last_name': 'user',
        }


    def test_user_signup_success(self):
        request = self.factory.post(self.endpoint, self.valid_payload)
        response = SignupAPIView.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], self.valid_payload['username'])
        self.assertIsNotNone(response.data['token'])


    def test_user_signup_required_fields(self):
        request = self.factory.post(self.endpoint, {})
        response = SignupAPIView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['username'][0].code, 'required')
        self.assertEqual(response.data['errors']['password'][0].code, 'required')
        self.assertEqual(response.data['errors']['first_name'][0].code, 'required')
        self.assertEqual(response.data['errors']['last_name'][0].code, 'required')


    def test_user_signup_blank_username(self):
        request_body = {
            'username': '',
            'password': 'test@123',
            'first_name': 'test',
            'last_name': 'user',
        }
        request = self.factory.post(self.endpoint, request_body)
        response = SignupAPIView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['username'][0].code, 'blank')


    def test_user_password_validation(self):
        request = self.factory.post(self.endpoint, {'password': 'test'})
        response = SignupAPIView.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['errors']['password'][0].title(),
            'Ensure This Field Has At Least 8 Characters.'
        )


    def test_user_username_already_exists(self):
        UserFactory(**self.valid_payload)
        request = self.factory.post(self.endpoint, self.valid_payload)
        response2 = SignupAPIView.as_view()(request)

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.data['errors']['username'][0].code, 'unique')
