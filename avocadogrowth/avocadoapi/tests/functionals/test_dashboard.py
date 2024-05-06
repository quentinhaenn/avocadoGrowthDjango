from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from avocadoapi.repositories.repository_factory import RepositoryFactory


class TestDashboard(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            "email"     : "test@test.com",
            "password"  : "testpassword",
            "username"  : "testuser",
            "first_name": "test",
            "last_name" : "user",
        }
        self.user_repo = RepositoryFactory.create_repository("user")
        self.user_repo.create(**self.credentials)

    def test_access_dashboard(self):
        user = self.user_repo.get(email=self.credentials['email'])
        model = get_user_model()
        assert isinstance(user, model)
        assert user is not None
        # send login data
        response = self.client.post('/api/login/', self.credentials, follow=True)
        # should be logged in now, and redirected to dashboard
        self.assertRedirects(response, '/api/dashboard/')
        # check if user is contained in content
        self.assertIn(b"user", response.content)
        self.assertIn(b"comments", response.content)
        self.assertIn(b"requests", response.content)
