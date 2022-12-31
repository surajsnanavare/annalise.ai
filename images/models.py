from django.db import models
from core.models import BaseModel


class Image(BaseModel):
    """
    A class that defines Image model
    """
    name = models.CharField(max_length=50)
    path = models.ImageField(upload_to='images', blank=True, null=True)

    def delete(self, *args, **kwargs):
        """
        Delete the image of menu item when item is deleted
        """
        self.path.storage.delete(self.path.name)
        super().delete()


class ImageTags(BaseModel):
    """
    A class that defines tags for image
    """
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='tags')
    label = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
