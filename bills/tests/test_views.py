import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Bill
from accounts.models import Profile

class BillViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_superuser = os.environ.get('TEST_SUPERUSER_USERNAME', 'supertest')
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        cls.superuser = User.objects.create_superuser(
            username=test_superuser, password=test_password
        )
        cls.user = User.objects.create_user(
            username=test_user, password=test_password
        )
        cls.profile = cls.user.profile

        cls.bill = Bill.objects.create(
            institution_name="Hospital Santo Amaro",
            payment_details="Consulta de teste",
            amount=100.00
        )

    def test_list_view_redirects_if_not_logged_in(self):
        list_url = reverse('bill_list')
        login_url = reverse('user-login')
        expected_redirect_url = f'{login_url}?next={list_url}'
        response = self.client.get(list_url)
        self.assertRedirects(response, expected_redirect_url)

    def test_list_view_is_accessible_if_logged_in(self):
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')
        
        self.client.login(username=test_user, password=test_password)
        response = self.client.get(reverse('bill_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/bill_list.html')
        self.assertContains(response, self.bill.institution_name)

    def test_create_view_get_page(self):
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_user, password=test_password)
        response = self.client.get(reverse('bill_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/billcreate.html')

    def test_create_view_post_creates_bill(self):
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_user, password=test_password)
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_create'), {
            'institution_name': 'Nova Instituição',
            'payment_details': 'Novo Pagamento',
            'amount': 250.75,
        })
        self.assertEqual(Bill.objects.count(), initial_bill_count + 1)
        self.assertRedirects(response, reverse('bill_list'))

    def test_update_view_post_updates_bill(self):
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_user, password=test_password)
        response = self.client.post(reverse('bill_update', args=[self.bill.slug]), {
            'institution_name': 'Nome Atualizado',
            'payment_details': self.bill.payment_details,
            'amount': self.bill.amount,
        })
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.institution_name, 'Nome Atualizado')
        self.assertRedirects(response, reverse('bill_list'))

    def test_delete_view_permission_denied_for_normal_user(self):
        test_user = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_user, password=test_password)
        response = self.client.get(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_view_post_by_superuser(self):
        test_superuser = os.environ.get('TEST_SUPERUSER_USERNAME', 'supertest')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'defaultpass123')

        self.client.login(username=test_superuser, password=test_password)
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(Bill.objects.count(), initial_bill_count - 1)
        self.assertRedirects(response, reverse('bill_list'))