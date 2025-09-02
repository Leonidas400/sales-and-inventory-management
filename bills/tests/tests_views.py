# bills/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Bill
from accounts.models import Profile

class BillViewsTest(TestCase):
    """Test suite for the views in the bills app."""

    @classmethod
    def setUpTestData(cls):
        """
        Configura dados iniciais para todos os testes.
        Cria um superusuário, um usuário normal com perfil e um objeto Bill.
        """
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

    # Testes para BillListView
    def test_bill_list_view_redirects_if_not_logged_in(self):
        """Verifica se usuários deslogados são redirecionados da lista."""
        list_url = reverse('bill_list')

        # --- CORREÇÃO APLICADA AQUI ---
        # Trocamos 'login' por 'account_login', que é um nome de URL comum.
        # Se o erro persistir, verifique o 'name' da sua URL de login
        # no arquivo accounts/urls.py e substitua aqui.
        login_url = reverse('account_login')
        
        expected_redirect_url = f'{login_url}?next={list_url}'
        
        response = self.client.get(list_url)
        self.assertRedirects(response, expected_redirect_url)

    def test_bill_list_view_accessible_if_logged_in(self):
        """Verifica se usuários logados podem acessar a lista."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/bill_list.html')
        self.assertContains(response, self.bill.institution_name)

    # Testes para BillCreateView
    def test_bill_create_view_get(self):
        """Verifica se a página de criação carrega para usuários logados."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/billcreate.html')

    def test_bill_create_view_post(self):
        """Verifica se uma nova conta pode ser criada via POST."""
        self.client.login(username='testuser', password='password123')
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_create'), {
            'institution_name': 'Nova Instituição',
            'payment_details': 'Novo Pagamento',
            'amount': 250.75,
        })
        self.assertEqual(Bill.objects.count(), initial_bill_count + 1)
        self.assertRedirects(response, reverse('bill_list'))

    # Testes para BillUpdateView
    def test_bill_update_view_post(self):
        """Verifica se uma conta pode ser atualizada por um usuário com perfil."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('bill_update', args=[self.bill.slug]), {
            'institution_name': 'Nome Atualizado',
            'payment_details': self.bill.payment_details,
            'amount': self.bill.amount,
        })
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.institution_name, 'Nome Atualizado')
        self.assertRedirects(response, reverse('bill_list'))

    # Testes para BillDeleteView
    def test_bill_delete_view_permission_for_normal_user(self):
        """Verifica se um usuário normal não pode deletar (requer superuser)."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(response.status_code, 403) # 403 Forbidden

    def test_bill_delete_view_by_superuser(self):
        """Verifica se um superusuário pode deletar uma conta."""
        self.client.login(username='superuser', password='password123')
        initial_bill_count = Bill.objects.count()
        response = self.client.post(reverse('bill_delete', args=[self.bill.pk]))
        self.assertEqual(Bill.objects.count(), initial_bill_count - 1)
        self.assertRedirects(response, reverse('bill_list'))