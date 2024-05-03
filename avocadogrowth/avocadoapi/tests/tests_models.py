from django.test import TestCase

from avocadoapi.models import User, Mentor, Comments, Stacks

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


def setUpUsers():
    User.objects.create(**user_john)
    User.objects.create(**user_jerry)


def setUpMentors():
    Mentor.objects.create(user=User.objects.get(email="jerry@doe.com"))


class UserTestCase(TestCase):

    def setUp(self):
        setUpUsers()

    def test_new_user(self):
        new_user = User(first_name="Jane", last_name="Doe", email="jane@doe.com", password="password")
        self.assertEqual(new_user.first_name, "Jane")
        self.assertEqual(new_user.last_name, "Doe")
        self.assertEqual(new_user.email, "jane@doe.com")
        self.assertEqual(new_user.password, "password")
        new_user.save()
        self.assertEqual(new_user.id, 3)

    def test_user_retrieving_with_email(self):
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.first_name, "John")
        self.assertEqual(john.last_name, "Doe")

    def test_user_retrieving_with_id(self):
        john = User.objects.get(id=1)
        self.assertEqual(john.first_name, "John")
        self.assertEqual(john.last_name, "Doe")

    def test_user_listing(self):
        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name, "John")
        self.assertEqual(users[1].first_name, "Jerry")

    def test_user_updating(self):
        john = User.objects.get(email="john@doe.com")
        john.first_name = "Johnny"
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.first_name, "Johnny")

    def test_user_deleting(self):
        john = User.objects.get(email="john@doe.com")
        john.delete()
        self.assertEqual(User.objects.count(), 1)
        assert not User.objects.filter(email="john@doe.com").exists()

    def test_user_deleting_all(self):
        User.objects.all().delete()
        self.assertEqual(User.objects.count(), 0)

    def test_user_deleting_with_id(self):
        User.objects.filter(id=1).delete()
        self.assertEqual(User.objects.count(), 1)
        assert not User.objects.filter(id=1).exists()

    def test_user_deleting_with_email(self):
        User.objects.filter(email="john@doe.com").delete()
        self.assertEqual(User.objects.count(), 1)
        assert not User.objects.filter(email="john@doe.com").exists()

    def test_user_cannot_have_same_email(self):
        with self.assertRaises(Exception):
            User.objects.create(**self.user_john)


class TestMentorModel(TestCase):
    def setUp(self):
        setUpUsers()
        User.objects.create(first_name="Jane", last_name="Doe", email="jane@doe.com", password="password")
        setUpMentors()

    def test_new_mentor(self):
        john = User.objects.get(email="john@doe.com")
        mentor = Mentor(user=john, description="I am a mentor", rating=4.5, is_available=True, history=10)
        mentor.save()
        self.assertEqual(mentor.user.first_name, "John")
        self.assertEqual(mentor.description, "I am a mentor")
        self.assertEqual(mentor.rating, 4.5)
        self.assertEqual(mentor.is_available, True)
        self.assertEqual(mentor.history, 10)

    def test_mentor_retrieving_with_user(self):
        jerry = User.objects.get(email="jerry@doe.com")
        mentor = Mentor.objects.get(user=jerry)
        self.assertEqual(mentor.user.first_name, "Jerry")
        self.assertEqual(mentor.description, "")
        self.assertEqual(mentor.rating, None)
        self.assertEqual(mentor.is_available, False)
        self.assertEqual(mentor.history, 0)

    def test_mentor_listing(self):
        mentors = Mentor.objects.all()
        self.assertEqual(len(mentors), 1)
        self.assertEqual(mentors[0].user.first_name, "Jerry")

    def test_mentor_updating(self):
        jerry = User.objects.get(email="jerry@doe.com")
        mentor = Mentor.objects.get(user=jerry)
        mentor.description = "I am a mentor"
        mentor.save()
        mentor = Mentor.objects.get(user=jerry)
        self.assertEqual(mentor.description, "I am a mentor")

    def test_mentor_deleting(self):
        jerry = User.objects.get(email="jerry@doe.com")
        mentor = Mentor.objects.get(user=jerry)
        mentor.delete()
        self.assertEqual(Mentor.objects.count(), 0)
        assert not Mentor.objects.filter(user=jerry).exists()

    def test_mentor_deleting_all(self):
        Mentor.objects.all().delete()
        self.assertEqual(Mentor.objects.count(), 0)

    def test_add_mentor_to_user(self):
        john = User.objects.get(email="john@doe.com")
        jerry = User.objects.get(email="jerry@doe.com")
        mentor = Mentor.objects.get(user=jerry)
        john.mentors.add(mentor)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.mentors.count(), 1)
        self.assertEqual(john.mentors.first().user.first_name, "Jerry")

    def test_remove_mentor_from_user(self):
        john = User.objects.get(email="john@doe.com")
        jerry = User.objects.get(email="jerry@doe.com")
        mentor = Mentor.objects.get(user=jerry)
        john.mentors.add(mentor)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.mentors.count(), 1)
        john.mentors.remove(mentor)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.mentors.count(), 0)


def setUpComments():
    john = User.objects.get(email="john@doe.com")
    jerry = User.objects.get(email="jerry@doe.com")
    mentor_jerry = Mentor.objects.get(user=jerry)
    comment = Comments(comment="Great mentor", rating=5, from_user=john, to_user=mentor_jerry)
    comment.save()


class TestCommentsModel(TestCase):
    def setUp(self):
        setUpUsers()
        setUpMentors()

    def test_new_comment(self):
        setUpComments()
        john = User.objects.get(email="john@doe.com")
        mentor_jerry = Mentor.objects.get(user=User.objects.get(email="jerry@doe.com"))
        comment = Comments.objects.get(from_user=john)
        self.assertEqual(comment.comment, "Great mentor")
        self.assertEqual(comment.rating, 5)
        self.assertEqual(comment.from_user.first_name, "John")
        comment = Comments.objects.get(from_user=john)
        self.assertEqual(comment.to_user.user.first_name, "Jerry")
        self.assertEqual(comment.to_user, mentor_jerry)
        self.assertEqual(comment.comment, "Great mentor")
        self.assertEqual(comment.rating, 5)

    def test_comment_listing(self):
        setUpComments()
        john = User.objects.get(email="john@doe.com")
        jerry = User.objects.get(email="jerry@doe.com")
        mentor_jerry = Mentor.objects.get(user=jerry)
        comment = Comments(comment="not so great mentor", rating=2, from_user=john, to_user=mentor_jerry)
        comment.save()
        comments = Comments.objects.all()
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].comment, "Great mentor")
        self.assertEqual(comments[1].comment, "not so great mentor")

    def test_comment_retrieving_with_user(self):
        setUpComments()
        john = User.objects.get(email="john@doe.com")
        comment = Comments.objects.get(from_user=john)
        self.assertEqual(comment.comment, "Great mentor")
        self.assertEqual(comment.rating, 5)
        self.assertEqual(comment.from_user.first_name, "John")
        self.assertEqual(comment.to_user.user.first_name, "Jerry")

    def test_comment_retrieving_with_mentor(self):
        setUpComments()
        jerry = Mentor.objects.get(user=User.objects.get(email="jerry@doe.com"))
        comment = Comments.objects.get(to_user=jerry)
        self.assertEqual(comment.comment, "Great mentor")
        self.assertEqual(comment.rating, 5)
        self.assertEqual(comment.from_user.first_name, "John")
        self.assertEqual(comment.to_user.user.first_name, "Jerry")

    def comment_updating(self):
        setUpComments()
        comment = Comments.objects.get(from_user=User.objects.get(email="john@doe.com"))
        comment.comment = "not so great mentor"
        comment.save()
        comment = Comments.objects.get(from_user=User.objects.get(email="john@doe.com"))
        self.assertEqual(comment.comment, "not so great mentor")

    def test_comment_deleting(self):
        setUpComments()
        comment = Comments.objects.get(from_user=User.objects.get(email="john@doe.com"))
        comment.delete()
        self.assertEqual(Comments.objects.count(), 0)
        assert not Comments.objects.filter(from_user=User.objects.get(email="john@doe.com")).exists()

    def test_comment_deleting_all(self):
        setUpComments()
        Comments.objects.all().delete()
        self.assertEqual(Comments.objects.count(), 0)


class TestStacksModel(TestCase):
    def setUp(self):
        setUpUsers()
        setUpMentors()
        setUpComments()

    def test_new_stack(self):
        python = Stacks(tag="Python")
        python.save()
        self.assertEqual(python.tag, "Python")
        self.assertEqual(python.id, 1)
        python = Stacks.objects.get(tag="Python")
        self.assertEqual(python.tag, "Python")
        self.assertEqual(python.id, 1)

    def test_add_stack_to_user(self):
        python = Stacks(tag="Python")
        python.save()
        john = User.objects.get(email="john@doe.com")
        john.learning_stacks.add(python)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.learning_stacks.count(), 1)
        self.assertEqual(john.learning_stacks.first().tag, "Python")

    def test_remove_stack_from_user(self):
        python = Stacks(tag="Python")
        python.save()
        john = User.objects.get(email="john@doe.com")
        john.learning_stacks.add(python)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.learning_stacks.count(), 1)
        john.learning_stacks.remove(python)
        john.save()
        john = User.objects.get(email="john@doe.com")
        self.assertEqual(john.learning_stacks.count(), 0)

    def test_add_stack_to_mentor(self):
        python = Stacks(tag="Python")
        python.save()
        jerry = User.objects.get(email="jerry@doe.com")
        mentor_jerry = Mentor.objects.get(user=jerry)
        mentor_jerry.stacks.add(python)
        mentor_jerry.save()
        mentor_jerry = Mentor.objects.get(user=jerry)
        self.assertEqual(mentor_jerry.stacks.count(), 1)
        self.assertEqual(mentor_jerry.stacks.first().tag, "Python")

    def test_remove_stack_from_mentor(self):
        python = Stacks(tag="Python")
        python.save()
        jerry = User.objects.get(email="jerry@doe.com")
        mentor_jerry = Mentor.objects.get(user=jerry)
        mentor_jerry.stacks.add(python)
        mentor_jerry.save()
        mentor_jerry = Mentor.objects.get(user=jerry)
        self.assertEqual(mentor_jerry.stacks.count(), 1)
        mentor_jerry.stacks.remove(python)
        mentor_jerry.save()
        mentor_jerry = Mentor.objects.get(user=jerry)
        self.assertEqual(mentor_jerry.stacks.count(), 0)

    def test_stack_listing(self):
        python = Stacks(tag="Python")
        python.save()
        java = Stacks(tag="Java")
        java.save()
        stacks = Stacks.objects.all()
        self.assertEqual(len(stacks), 2)
        self.assertEqual(stacks[0].tag, "Python")
        self.assertEqual(stacks[1].tag, "Java")

    def test_stack_retrieving_with_id(self):
        python = Stacks(tag="Python")
        python.save()
        stack = Stacks.objects.get(id=1)
        self.assertEqual(stack.tag, "Python")

    def test_stack_retrieving_with_tag(self):
        python = Stacks(tag="Python")
        python.save()
        stack = Stacks.objects.get(tag="Python")
        self.assertEqual(stack.tag, "Python")

    def test_stack_updating(self):
        python = Stacks(tag="Python")
        python.save()
        python.tag = "Python3"
        python.save()
        stack = Stacks.objects.get(tag="Python3")
        self.assertEqual(stack.tag, "Python3")

    def test_stack_deleting(self):
        python = Stacks(tag="Python")
        python.save()
        python.delete()
        self.assertEqual(Stacks.objects.count(), 0)
        assert not Stacks.objects.filter(tag="Python").exists()

    def test_stack_deleting_all(self):
        python = Stacks(tag="Python")
        python.save()
        java = Stacks(tag="Java")
        java.save()
        Stacks.objects.all().delete()
        self.assertEqual(Stacks.objects.count(), 0)
