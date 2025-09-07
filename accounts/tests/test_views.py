import os
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
        
        reg_username = os.environ.get('TEST_REG_USERNAME', 'new_user_reg')
        reg_email = os.environ.get('TEST_REG_EMAIL', 'register@example.com')
        reg_password = os.environ.get('TEST_REG_PASSWORD', 'a-very-secure-password-123')

        initial_user_count = User.objects.count()
        response = self.client.post(reverse('user-register'), {
            'username': reg_username,
            'email': reg_email,
            'password1': reg_password,
            'password2': reg_password,
        })
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertRedirects(response, reverse('user-login'))


class GeneralAccountViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')
        superuser_user = os.environ.get('TEST_SUPERUSER_USERNAME', 'supertest')
        customer_fname = os.environ.get('TEST_CUSTOMER_FNAME', 'John')
        customer_lname = os.environ.get('TEST_CUSTOMER_LNAME', 'Doe')
        vendor_name = os.environ.get('TEST_VENDOR_NAME', 'Test Vendor')

        cls.user = User.objects.create_user(username=test_user, password=test_password)
        cls.superuser = User.objects.create_superuser(username=superuser_user, password=test_password)
        cls.customer = Customer.objects.create(first_name=customer_fname, last_name=customer_lname)
        cls.vendor = Vendor.objects.create(name=vendor_name)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('user-profile'))
        self.assertRedirects(response, f"{reverse('user-login')}?next={reverse('user-profile')}")

    def test_profile_view_loads_for_logged_in_user(self):
    
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_user, password=test_password)
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_customer_list_view_loads_for_logged_in_user(self):
        
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')
        
        self.client.login(username=test_user, password=test_password)
        
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer_list.html')
        self.assertContains(response, self.customer.first_name)