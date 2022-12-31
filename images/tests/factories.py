import factory
from images.models import Image, ImageTags


class ImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Image
    
    name = factory.Sequence(lambda n: "image_%03d" % n)


class ImageTagsFactory(factory.django.DjangoModelFactory):
   
    class Meta:
        model = ImageTags
    
    image = factory.SubFactory(ImageFactory)
    label = factory.Sequence(lambda n: "label_%03d" % n)
    value = factory.Sequence(lambda n: "value_%03d" % n)
