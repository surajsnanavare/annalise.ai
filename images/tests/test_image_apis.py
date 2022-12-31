import os
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from users.test.factories import UserFactory
from images.api.views import ImageView
from django.conf import settings


class TestImageAPIs(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.factory = APIRequestFactory()


    def test_unauthorized_users_can_not_upload_image(self):
        file_path = os.path.join(settings.BASE_DIR, 'images/tests/sample.jpeg')
        with open(file_path, 'rb') as sampleFile:
            
            request = self.factory.post('/image', {
                'path': sampleFile,
                'name': 'Sample File'
            }, format='multipart')

            response = ImageView.as_view({'post': 'create'})(request)
            self.assertEqual(response.status_code, 403)


    def test_authorized_users_can_upload_image(self):
        file_path = os.path.join(settings.BASE_DIR, 'images/tests/sample.jpeg')
        with open(file_path, 'rb') as sampleFile:
            
            request = self.factory.post('/image', {
                'path': sampleFile,
                'name': 'Sample File'
            }, format='multipart')

            force_authenticate(request=request, user=self.user)
            response = ImageView.as_view({'post': 'create'})(request)
            
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['name'], 'Sample File')

