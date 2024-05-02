from . import mentors, stacks, users, requests


class RepositoryFactory:
    def __init__(self, model):
        self.model = model

    @classmethod
    def create_repository(cls, model):
        if model == 'mentor':
            return mentors.MentorRepository()
        elif model == 'stack':
            return stacks.StackRepository()
        elif model == 'user':
            return users.UserRepository()
        elif model == 'request':
            return requests.RequestRepository()
        raise ValueError(f"Model {model} not found")