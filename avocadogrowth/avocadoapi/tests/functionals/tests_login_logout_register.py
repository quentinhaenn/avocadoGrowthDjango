from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from avocadoapi.repositories.repository_factory import RepositoryFactory


class TestLoginLogoutRegister(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            "email"   : "test@test.com",
            "password": "testpassword"
        }
        self.user_repo = RepositoryFactory.create_repository("user")
        self.user_repo.create(**self.credentials)

    def test_register(self):
        response = self.client.post(
            "/api/register/",
            {
                "email"   : "test@register.com",
                "password": "testpassword"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'User created successfully')

    def test_register_missing_data(self):
        response = self.client.post(
            "/api/register/",
            {}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Email is required')

    def test_register_missing_password(self):
        response = self.client.post(
            "/api/register/",
            {
                'email': 'test@test.com'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Password is required')

    def test_login(self):
        user = self.user_repo.get(email=self.credentials['email'])
        model = get_user_model()
        assert isinstance(user, model)
        assert user is not None
        # send login data
        response = self.client.post('/api/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertEqual(response.status_code, 200)
        # check if logged in
        self.assertEqual(response.content, b'Welcome, 1!')
