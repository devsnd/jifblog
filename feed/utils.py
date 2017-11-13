
import uuid

from django.db.models import ManyToOneRel, ManyToManyField, ManyToManyRel
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPathWithUUID(object):
    path = "{0}/{1}.{2}"

    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.rsplit('.')[-1]
        return self.path.format(self.sub_path, uuid.uuid4(), ext)


def generate_auto_model_admin(model, hidden_fields=('id',), **kwargs):
    from django.contrib import admin
    list_display = ['id']
    for field in model._meta.get_fields():
        # do not print the many to one relations in this admin
        if isinstance(field, ManyToOneRel) or isinstance(field, ManyToManyRel) or isinstance(field, ManyToManyField):
            continue
        if field.name not in hidden_fields:
            list_display.append(field.name)

    cls_attrs = {
        'list_display': list_display
    }
    cls_attrs.update(kwargs)
    admincls = type(
        model.__qualname__,
        (admin.ModelAdmin,),
        cls_attrs
    )
    return admincls


def generate_and_register_admin(model):
    from django.contrib import admin
    admin.site.register(model, generate_auto_model_admin(model))
