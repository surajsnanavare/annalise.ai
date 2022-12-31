from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from images.api import serializers
from images.models import Image, ImageTags


class ImageView(viewsets.ModelViewSet):
    """ View responsible to manage orders """
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ImageSerializer


class ImageTagView(viewsets.ModelViewSet):
    """ View responsible to manage orders """
    queryset = ImageTags.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ImageTagSerializer

    def get_queryset(self):
        image_id = self.kwargs.get('image_pk', None)
        return self.queryset.filter(image__id=image_id)


class ImageTagBulkView(viewsets.ModelViewSet):
    """ View responsible to manage orders """
    queryset = ImageTags.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ImageTagBulkSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
