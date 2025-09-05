from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Bill
from accounts.models import Profile

class BillViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='superuser', password='password123'
        )
        cls.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        cls.profile = cls.user.profile

        cls.bill = Bill.objects.create(
            institution_name="Hospital Teste",
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
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/bill_list.html')
        self.assertContains(response, self.bill.institution_name)

    def test_create_view_get_page(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/billcreate.html')

    def test_create_view_post_creates_bill(self):
        self.client.login(username='testuser', password='password123')
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_create'), {
            'institution_name': 'Nova Instituição',
            'payment_details': 'Novo Pagamento',
            'amount': 250.75,
        })
        self.assertEqual(Bill.objects.count(), initial_bill_count + 1)
        self.assertRedirects(response, reverse('bill_list'))

    def test_update_view_post_updates_bill(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('bill_update', args=[self.bill.slug]), {
            'institution_name': 'Nome Atualizado',
            'payment_details': self.bill.payment_details,
            'amount': self.bill.amount,
        })
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.institution_name, 'Nome Atualizado')
        self.assertRedirects(response, reverse('bill_list'))

    def test_delete_view_permission_denied_for_normal_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_view_post_by_superuser(self):
        self.client.login(username='superuser', password='password123')
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(Bill.objects.count(), initial_bill_count - 1)
        self.assertRedirects(response, reverse('bill_list'))