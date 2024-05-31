import unittest
from django.test import Client
from django.urls import reverse

from .models import Customer 

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.customer = Customer.objects.create(
            email='test@example.com', 
            password='testpass123'
        )

    def test_get_login_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid(self):
        response = self.client.post(self.url, {
            'email': self.customer.email,
            'password': 'testpass123' 
        })
        self.assertRedirects(response, reverse('homepage'))

    def test_login_invalid_password(self):
        response = self.client.post(self.url, {
            'email': self.customer.email,
            'password': 'wrongpass'
        })
        self.assertFormError(response, 'form', 'password', 'Invalid!!')

    def test_login_invalid_email(self):
        response = self.client.post(self.url, {
            'email': 'wrong@email.com',
            'password': 'testpass123'
        })
        self.assertFormError(response, 'form', None, 'Invalid!!')
