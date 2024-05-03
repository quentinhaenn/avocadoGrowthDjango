"""
Factory class to create repository objects based on the model name.
"""
from . import mentors, stacks, users, requests


class RepositoryFactory:
    # pylint: disable=too-few-public-methods
    def __init__(self, model):
        self.model = model

    @classmethod
    def create_repository(cls, model):
        """
        Create a repository object based on the model name.
        """
        if model == "mentor":
            return mentors.MentorRepository()
        if model == "stack":
            return stacks.StackRepository()
        if model == "user":
            return users.UserRepository()
        if model == "request":
            return requests.RequestRepository()
        raise ValueError(f"Model {model} not found")
