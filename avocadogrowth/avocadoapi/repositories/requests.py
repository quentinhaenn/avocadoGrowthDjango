from ..models import Requests
from .base import BaseRepository


class RequestRepository(BaseRepository):
    model = Requests

    @classmethod
    def get_requests_by_user(cls, user):
        return cls.model.objects.filter(from_user=user)

    @classmethod
    def get_requests_by_mentor(cls, mentor):
        return cls.model.objects.filter(to_mentor=mentor)
