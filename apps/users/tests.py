from django.test import TestCase
from django.urls import reverse
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type='OWNER'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.user_type, 'OWNER')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)