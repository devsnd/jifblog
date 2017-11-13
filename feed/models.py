from django.db import models

from .utils import UploadToPathWithUUID


class GifImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=UploadToPathWithUUID('images'))
    caption = models.TextField(default='', blank=True, null=True)
    bgcolor = models.CharField(max_length=6)
