import os
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from users.test.factories import UserFactory
from images.tests.factories import ImageFactory, ImageTagsFactory
from images.api.views import ImageTagView
from django.conf import settings


class TestImageTagAPIs(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.factory = APIRequestFactory()
        self.image = ImageFactory()
        self.payload = {
            'image': self.image.id,
            'label': 'label1',
            'value': 'value1'
        }
        self.endpoint = '/image/${}/tags'.format(self.image.id)

    def test_unauthorized_users_can_not_add_tags(self):
        request = self.factory.post(self.endpoint, self.payload)
        response = ImageTagView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)

    def test_authorized_users_can_add_tags(self):
        request = self.factory.post(self.endpoint, self.payload)
        force_authenticate(request=request, user=self.user)
        response = ImageTagView.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['label'], self.payload['label'])
        self.assertEqual(response.data['value'], self.payload['value'])

    def test_required_fields_in_add_tags(self):
        request = self.factory.post(self.endpoint, {})
        force_authenticate(request=request, user=self.user)
        response = ImageTagView.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['label'][0].code, 'required')
        self.assertEqual(response.data['errors']['value'][0].code, 'required')

    def test_unauthorized_users_can_not_update_tags(self):
        image_tag = ImageTagsFactory(image=self.image)
        endpoint = "/image/{}/tags/{}".format(self.image.id, image_tag.id)
        request = self.factory.patch(endpoint, {'value': 'new'})
        response = ImageTagView.as_view({'patch': 'partial_update'})(
            request,
            pk=image_tag.id,
            image_pk=self.image.pk
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_users_can_update_tags(self):
        image_tag = ImageTagsFactory(image=self.image)
        endpoint = "/image/{}/tags/{}".format(self.image.id, image_tag.id)
        request = self.factory.patch(endpoint, {'value': 'new'})

        force_authenticate(request=request, user=self.user)
        response = ImageTagView.as_view({'patch': 'partial_update'})(
            request,
            pk=image_tag.id,
            image_pk=self.image.pk
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['value'], 'new')
