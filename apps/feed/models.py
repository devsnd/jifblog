from django.db import models
from django.utils import timezone

from .utils import UploadToPathWithUUID


class GifImage(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    image = models.ImageField(upload_to=UploadToPathWithUUID('images'))
    caption = models.TextField(default='', blank=True, null=True)
    bgcolor = models.CharField(max_length=6)
