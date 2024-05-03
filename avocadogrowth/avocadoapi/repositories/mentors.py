"""
This module contains the repository class for the Mentor model.
"""
from ..models import Mentor
from .base import BaseRepository


class MentorRepository(BaseRepository):
    model = Mentor

    @classmethod
    def get_mentor_by_stack(cls, stack):
        # pylint: disable=missing-function-docstring
        mentors_qs = cls.model.objects.filter(stacks__tag=stack).order_by("rating")
        mentors = [mentor for mentor in mentors_qs if mentor.is_available]
        return mentors

    @classmethod
    def add_stack(cls, mentor, stack):
        # pylint: disable=missing-function-docstring
        mentor.stacks.add(stack)
        mentor.save()

    @classmethod
    def remove_stack(cls, mentor, stack):
        # pylint: disable=missing-function-docstring
        mentor.stacks.remove(stack)
        mentor.save()

    @classmethod
    def get_stacks(cls, mentor):
        # pylint: disable=missing-function-docstring
        return mentor.stacks.all()

    @classmethod
    def set_available(cls, mentor):
        # pylint: disable=missing-function-docstring
        if not mentor.is_available:
            mentor.is_available = True
            mentor.save()
        else:
            raise ValueError("Mentor is already available")
