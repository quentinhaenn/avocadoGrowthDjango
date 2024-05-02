from django.core.exceptions import ObjectDoesNotExist


class BaseRepository:
    model = None

    @classmethod
    def get(cls, **kwargs):
        try:
            return cls.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def all(cls):
        return cls.model.objects.all()

    @classmethod
    def filter(cls, **kwargs):
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()
