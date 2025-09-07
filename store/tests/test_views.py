# store/tests/test_views.py

import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Category, Item, Delivery
from accounts.models import Profile, Vendor, Customer
from transactions.models import Sale

class StoreViewPermissionsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Cria usuários e objetos para testar as permissões."""
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        cls.category = Category.objects.create(name='Categoria Teste')
        # Vendor é necessário para criar um Item
        vendor = Vendor.objects.create(name='Fornecedor Padrão')
        cls.item = Item.objects.create(
            name='Item Teste',
            price=100,
            category=cls.category,
            vendor=vendor,
            description="Descrição Padrão"
        )

    def test_superuser_views_accessible_by_superuser(self):
        """Verifica se um superusuário pode acessar as views de update/delete."""
        self.client.login(username='superuser', password='password123')
        urls_to_check = [
            reverse('product-update', args=[self.item.slug]),
            reverse('product-delete', args=[self.item.slug]),
        ]
        for url in urls_to_check:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Superuser failed to access {url}")

    def test_superuser_views_denied_for_normal_user(self):
        """Verifica se um usuário normal é bloqueado das views de update/delete."""
        self.client.login(username='testuser', password='password123')
        urls_to_check = [
            reverse('product-update', args=[self.item.slug]),
            reverse('product-delete', args=[self.item.slug]),
        ]
        for url in urls_to_check:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403, f"Normal user was not denied access to {url}")


class DashboardViewTest(TestCase):

    def setUp(self):
        """Cria um usuário para os testes de dashboard."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_dashboard_view_loads_correctly(self):
        """Verifica se a página do dashboard carrega e usa o template correto."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/dashboard.html')
        self.assertIn('items_count', response.context)


class ProductViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.category = Category.objects.create(name='Categoria Produto')
        cls.vendor = Vendor.objects.create(name='Fornecedor Produto')
        cls.item = Item.objects.create(
            name='Produto A',
            price=50,
            category=cls.category,
            vendor=cls.vendor,
            description="Descrição do Produto A"
        )

    def test_product_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('productslist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_product_create_view_post(self):
        """Verifica a criação de um novo produto com todos os campos obrigatórios."""
        self.client.login(username='testuser', password='password123')
        initial_item_count = Item.objects.count()
        
        # --- CORREÇÃO APLICADA AQUI ---
        response = self.client.post(reverse('product-create'), {
            'name': 'Produto Novo',
            'category': self.category.pk,
            'price': 150,
            'quantity': 10,
            'description': 'Uma descrição para o produto novo.', # Campo obrigatório adicionado
            'vendor': self.vendor.pk                         # Campo obrigatório adicionado
        })
        
        self.assertEqual(Item.objects.count(), initial_item_count + 1)
        self.assertRedirects(response, "/products/")


class AjaxViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        category = Category.objects.create(name='Cat AJAX')
        vendor = Vendor.objects.create(name='Fornecedor AJAX')
        Item.objects.create(
            name='Item AJAX Test',
            price=10,
            category=category,
            vendor=vendor,
            description="Desc"
        )

    def test_get_items_ajax_view(self):
        """Verifica se a view AJAX de itens retorna JSON corretamente."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('get_items'),
            {'term': 'AJAX'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], 'Item AJAX Test')