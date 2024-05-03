from django.test import TestCase
from avocadoapi.models import User, Mentor, Stacks, Requests
from avocadoapi.repositories.repository_factory import RepositoryFactory

user_john = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@doe.com",
    "password": "password",
}
user_jerry = {
    "first_name": "Jerry",
    "last_name": "Doe",
    "email": "jerry@doe.com",
    "password": "password",
}

user_jane = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@doe.com",
    "password": "password",
}

stack_list = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "go",
    "rust",
    "scala",
    "r",
    "perl",
    "haskell",
    "shell",
    "powershell",
    "sql",
    "nosql",
    "Data Science",
    "Data",
    "Data Analysis",
    "Data Engineering",
    "Data Visualization",
    "Machine Learning",
]

stacks_jerry = [
    "python",
    "java",
    "Data Science",
    "Data Analysis",
    "Data Engineering",
    "Data Visualization",
    "Machine Learning",
]
stacks_john = [
    "javascript",
    "typescript",
    "c++",
    "c#",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "go",
    "rust",
    "scala",
    "r",
    "perl",
    "haskell",
    "shell",
    "powershell",
    "sql",
    "nosql",
]
stacks_jane = ["python", "java", "javascript", "typescript"]


def setUpUsers():
    User.objects.create(**user_john)
    User.objects.create(**user_jerry)
    User.objects.create(**user_jane)


def setUpMentors():
    Mentor.objects.create(user=User.objects.get(email="john@doe.com"))
    Mentor.objects.create(user=User.objects.get(email="jerry@doe.com"))


def setUpStacks():
    for stack in stack_list:
        Stacks.objects.create(tag=stack)


def setUpLearningStacks():
    user_john = User.objects.get(email="john@doe.com")
    mentor_john = Mentor.objects.get(user=user_john)
    user_jane = User.objects.get(email="jane@doe.com")
    for stack in stacks_jane:
        user_jane.learning_stacks.add(Stacks.objects.get(tag=stack))
        user_jane.save()

    for stack in stacks_john:
        mentor_john.stacks.add(Stacks.objects.get(tag=stack))
        mentor_john.save()


class TestRepositoryFactory(TestCase):
    def test_repository_factory(self):
        user_repo = RepositoryFactory.create_repository("user")
        assert user_repo.model == User

        mentor_repo = RepositoryFactory.create_repository("mentor")
        assert mentor_repo.model == Mentor

        stack_repo = RepositoryFactory.create_repository("stack")
        assert stack_repo.model == Stacks

        request_repo = RepositoryFactory.create_repository("request")
        assert request_repo.model == Requests


class TestUserRepository(TestCase):
    def setUp(self):
        setUpUsers()
        setUpMentors()
        setUpStacks()
        setUpLearningStacks()

    def test_basic_user_repository(self):
        user = User.objects.get(email="john@doe.com")
        user_repo = RepositoryFactory.create_repository("user")
        user_by_repo = user_repo.get(email="john@doe.com")
        assert user == user_by_repo

    def test_get_mentor_infos(self):
        user_repo = RepositoryFactory.create_repository("user")
        mentor_repo = RepositoryFactory.create_repository("mentor")
        john = user_repo.get(email="john@doe.com")
        mentor = mentor_repo.get(user=john)
        mentor_infos = user_repo.get_mentor_infos(john)
        assert mentor_infos == mentor

    def test_is_mentor(self):
        user_repo = RepositoryFactory.create_repository("user")
        john = user_repo.get(email="john@doe.com")
        jane = user_repo.get(email="jane@doe.com")
        assert user_repo.is_mentor(john)
        assert not user_repo.is_mentor(jane)

    def test_get_mentors(self):
        user_repo = RepositoryFactory.create_repository("user")
        mentor_repo = RepositoryFactory.create_repository("mentor")
        john = user_repo.get(email="john@doe.com")
        jerry = mentor_repo.get(user=user_repo.get(email="jerry@doe.com"))
        user_repo.add_mentor(john, jerry)
        mentors = user_repo.get_mentors(john)
        assert mentors.count() == 1
        assert mentors.first() == jerry

    def test_remove_mentor(self):
        user_repo = RepositoryFactory.create_repository("user")
        mentor_repo = RepositoryFactory.create_repository("mentor")
        john = user_repo.get(email="john@doe.com")
        jerry = user_repo.get(email="jerry@doe.com")
        mentor = mentor_repo.get(user=jerry)
        user_repo.add_mentor(john, mentor)
        assert john.mentors.count() == 1
        user_repo.remove_mentor(john, mentor)
        assert john.mentors.count() == 0

    def test_add_learning_stack(self):
        user_repo = RepositoryFactory.create_repository("user")
        john = user_repo.get(email="john@doe.com")
        actual_stacks = john.learning_stacks.count()
        user_repo.add_learning_stack(john, "scala")
        assert john.learning_stacks.count() == actual_stacks + 1

    def test_remove_learning_stack(self):
        user_repo = RepositoryFactory.create_repository("user")
        jane = user_repo.get(email="jane@doe.com")
        actual_stacks = jane.learning_stacks.all()
        nb_stacks = actual_stacks.count()
        assert actual_stacks.filter(tag="python").exists()
        user_repo.remove_learning_stack(jane, "python")
        assert jane.learning_stacks.count() == nb_stacks - 1


class TestMentorRepository(TestCase):
    def setUp(self):
        setUpUsers()
        setUpMentors()
        setUpStacks()
        setUpLearningStacks()

    def test_basic_mentor_repository(self):
        user = RepositoryFactory.create_repository("user").get(email="john@doe.com")
        mentor = Mentor.objects.get(user=user)
        mentor_repo = RepositoryFactory.create_repository("mentor")
        mentor_by_repo = mentor_repo.get(user=user)
        assert mentor == mentor_by_repo

    def test_get_mentor_by_stack(self):
        mentor_repo = RepositoryFactory.create_repository("mentor")
        user_repo = RepositoryFactory.create_repository("user")
        mentors = mentor_repo.get_mentor_by_stack("python")
        assert len(mentors) == 0
        mentors = mentor_repo.get_mentor_by_stack("javascript")
        assert len(mentors) == 0
        mentor_john = mentor_repo.get(user=user_repo.get(email="john@doe.com"))
        mentor_repo.set_available(mentor_john)
        mentors = mentor_repo.get_mentor_by_stack("javascript")
        assert mentors[0].user == user_repo.get(email="john@doe.com")


class TestStackRepository(TestCase):
    def setUp(self):
        setUpUsers()
        setUpMentors()
        setUpStacks()
        setUpLearningStacks()

    def test_basic_stack_repository(self):
        stack = Stacks.objects.get(tag="python")
        stack_repo = RepositoryFactory.create_repository("stack")
        stack_by_repo = stack_repo.get(tag="python")
        assert stack == stack_by_repo

    def test_get_all_stacks(self):
        stack_repo = RepositoryFactory.create_repository("stack")
        stacks = stack_repo.all()
        assert stacks.count() == len(stack_list)

    def test_stack_trie(self):
        stack_repo = RepositoryFactory.create_repository("stack")
        stack_repo.create_trie()
        assert stack_repo.autocomplete("py") == ["python"]
        assert stack_repo.autocomplete("java") == ["java", "javascript"]
        assert stack_repo.autocomplete("Data") == [
            "data",
            "data science",
            "data analysis",
            "data engineering",
            "data visualization",
        ]
