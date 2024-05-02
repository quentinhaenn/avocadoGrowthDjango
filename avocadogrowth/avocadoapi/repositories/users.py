from django.contrib.auth import get_user_model
from .base import BaseRepository
from .mentors import MentorRepository
from .stacks import StackRepository


class UserRepository(BaseRepository):
    model = get_user_model()

    @classmethod
    def add_mentor(cls, user, mentor):
        user.mentors.add(mentor)
        user.save()

    @classmethod
    def remove_mentor(cls, user, mentor):
        user.mentors.remove(mentor)
        user.save()

    @classmethod
    def get_mentor_infos(cls, user):
        return MentorRepository.get(user=user)

    @classmethod
    def add_learning_stack(cls, user, stack_tag):
        stack = StackRepository.get(tag=stack_tag)
        user.learning_stacks.add(stack)
        user.save()

    @classmethod
    def remove_learning_stack(cls, user, stack_tag):
        stack = StackRepository.get(tag=stack_tag)
        user.learning_stacks.remove(stack)
        user.save()

    @classmethod
    def get_learning_stacks(cls, user):
        return user.learning_stacks.all()

    @classmethod
    def is_mentor(cls, user):
        return user.is_mentor()

    @classmethod
    def get_mentors(cls, user):
        return user.mentors.all()
