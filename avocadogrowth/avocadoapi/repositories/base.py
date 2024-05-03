"""
Abstract class for repository pattern
"""
from django.core.exceptions import ObjectDoesNotExist


class BaseRepository:
    model = None

    @classmethod
    def get(cls, **kwargs):
        # pylint: disable=missing-function-docstring
        try:
            return cls.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def all(cls):
        # pylint: disable=missing-function-docstring
        return cls.model.objects.all()

    @classmethod
    def filter(cls, **kwargs):
        # pylint: disable=missing-function-docstring
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        # pylint: disable=missing-function-docstring
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        # pylint: disable=missing-function-docstring
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        # pylint: disable=missing-function-docstring
        instance.delete()
