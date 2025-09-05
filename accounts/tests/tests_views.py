# accounts/tests/test_views.py

import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Profile, Customer, Vendor

class AuthViewsTest(TestCase):

    def test_register_view_get(self):
        """Verifica se a página de registro carrega corretamente."""
        response = self.client.get(reverse('user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_creates_user(self):
        """Verifica se o POST para registro cria um novo usuário."""
        initial_user_count = User.objects.count()
        response = self.client.post(reverse('user-register'), {
            'username': 'new_user',
            'email': 'new@email.com',
            'password1': 'a-strong-password123',
            'password2': 'a-strong-password123',
        })
        self.assertEqual(User.objects.count(), initial_user_count + 1)
        self.assertRedirects(response, reverse('user-login'))


class GeneralAccountViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Cria usuários e objetos para os testes."""
        cls.user = User.objects.create_user(username='testuser', password='password123')
        # Signal cria o Profile automaticamente
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        cls.customer = Customer.objects.create(first_name="João", last_name="Silva")
        cls.vendor = Vendor.objects.create(name="Fornecedor Teste")

    def test_profile_view_requires_login(self):
        """Verifica se a view de perfil redireciona se o usuário não estiver logado."""
        response = self.client.get(reverse('user-profile'))
        self.assertRedirects(response, f"{reverse('user-login')}?next={reverse('user-profile')}")

    def test_profile_view_loads_for_logged_in_user(self):
        """Verifica se a view de perfil carrega para um usuário logado."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_customer_list_view_loads_for_logged_in_user(self):
        """Verifica se a lista de clientes carrega."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/customer_list.html')
        self.assertContains(response, self.customer.first_name)
    
    def test_customer_create_view_post(self):
        """Verifica se um novo cliente pode ser criado via POST."""
        self.client.login(username='testuser', password='password123')
        initial_count = Customer.objects.count()
        response = self.client.post(reverse('customer_create'), {
            'first_name': 'Maria',
            'last_name': 'Santos',
            'loyalty_points': 50
        })
        self.assertEqual(Customer.objects.count(), initial_count + 1)
        self.assertRedirects(response, reverse('customer_list'))

    def test_staff_profile_crud_requires_superuser(self):
        """Verifica se as views de CRUD de Profile requerem superusuário."""
        self.client.login(username='testuser', password='password123')
        
        # Cria um segundo usuário para ser o alvo das operações
        target_user = User.objects.create_user(username='targetuser', password='password123')
        
        urls_to_check = [
            reverse('profile-create'),
            reverse('profile-update', args=[target_user.profile.pk]),
            reverse('profile-delete', args=[target_user.profile.pk]),
        ]
        for url in urls_to_check:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403, f"Acesso não foi negado para a URL: {url}")

    def test_get_customers_ajax_view(self):
        """Verifica a resposta da view AJAX get_customers."""
        self.client.login(username='testuser', password='password123')
        
        # Cria mais um cliente para testar o filtro
        Customer.objects.create(first_name='Joana', last_name='Pereira')
        
        url = reverse('get_customers')
        # Faz uma requisição POST AJAX
        response = self.client.post(
            url, 
            {'term': 'João'}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(len(data), 1) # Espera encontrar apenas o cliente 'João Silva'
        self.assertEqual(data[0]['label'], 'João Silva')