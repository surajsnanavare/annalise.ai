from rest_framework import serializers
from images.models import Image, ImageTags
from django.shortcuts import get_object_or_404


class ImageTagSerializer(serializers.ModelSerializer):
    """ Serializer for Image tag model """

    class Meta:
        model = ImageTags
        fields = ['id', 'image', 'label', 'value']


class ImageTagMinimalSerializer(serializers.ModelSerializer):
    """ Serializer for Image tag model """

    class Meta:
        model = ImageTags
        fields = ['id', 'label', 'value']


class ImageSerializer(serializers.ModelSerializer):
    """ Serializer for Images Model """
    tags = ImageTagMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'name', 'path', 'created', 'updated', 'tags']


class ImageTagBulkSerializer(serializers.Serializer):
    image =  serializers.UUIDField();
    tags = ImageTagMinimalSerializer(many=True)

    def create(self, validated_data):
        image_pk = validated_data.get('image')
        image_obj = get_object_or_404(Image, pk=image_pk)
        tags = validated_data.get('tags')
        
        _tags = []
        for tag in tags:
            tag_obj = ImageTags.objects.create(
                image=image_obj,
                **dict(tag)
            )
            _tags.append(tag_obj)
        
        return {
            'image': image_pk,
            'tags': _tags,
        }
