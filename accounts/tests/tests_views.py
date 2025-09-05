import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Profile, Customer, Vendor

class AuthViewsTest(TestCase):

    def test_register_view_get(self):
        response = self.client.get(reverse('user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_creates_user(self):
        initial_user_count = User.objects.count()
        response = self.client.post(reverse('user-register'), {
            'username': 'jorge_silveira',
            'email': 'jorge@email.com',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123',
        })
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertRedirects(response, reverse('user-login'))


class GeneralAccountViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='teste', password='senha123')
        cls.superuser = User.objects.create_superuser(username='superteste', password='senha123')
        cls.customer = Customer.objects.create(first_name="Jorge", last_name="Silveira")
        cls.vendor = Vendor.objects.create(name="Fornecedor Teste")

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('user-profile'))
        self.assertRedirects(response, f"{reverse('user-login')}?next={reverse('user-profile')}")

    def test_profile_view_loads_for_logged_in_user(self):
        self.client.login(username='teste', password='senha123')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_customer_list_view_loads_for_logged_in_user(self):
        self.client.login(username='teste', password='senha123')
        response = self.client.get(reverse('customer_list'))
        self