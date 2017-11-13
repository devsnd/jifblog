from django.contrib import admin

from .models import GifImage
from .utils import generate_and_register_admin

generate_and_register_admin(GifImage)
