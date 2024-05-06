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
        string = f"Welcome, {user.username if user.username else user.email}!"
        self.assertEqual(response.content, string.encode())

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/api/login/",
            {
                "email"   : "test@test.com",
                "password": "wrongpassword"
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'Invalid credentials')

    def test_login_missing_data(self):
        response = self.client.post(
            "/api/login/",
            {
                "email": "test@test.com",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Password is required')
        response = self.client.post(
            "/api/login/",
            {
                "password": "testpassword",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Email is required')

    def test_access_dashboard(self):
        user = self.user_repo.get(email=self.credentials['email'])
        model = get_user_model()
        assert isinstance(user, model)
        assert user is not None
        self.client.login(email=self.credentials['email'], password=self.credentials['password'])
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, 200)
        string = f"Welcome, {user.username if user.username else user.email}!"
        self.assertEqual(response.content, string.encode())

    def test_access_dashboard_unauthenticated(self):
        response = self.client.get('/api/dashboard/')
        self.assertRedirects(response, '/api/login/', status_code=302, target_status_code=204)

    def test_logout(self):
        user = self.user_repo.get(email=self.credentials['email'])
        model = get_user_model()
        assert isinstance(user, model)
        assert user is not None
        self.client.login(email=self.credentials['email'], password=self.credentials['password'])
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Logout successful')

    def test_logout_not_logged_in(self):
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'You are not logged in')
