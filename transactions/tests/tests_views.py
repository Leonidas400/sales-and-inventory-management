# transactions/tests/test_views.py

import json
from io import BytesIO
from openpyxl import load_workbook
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Sale, Purchase, SaleDetail
from store.models import Item, Category
from accounts.models import Customer, Vendor, Profile

class SaleViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        cls.customer = Customer.objects.create(first_name='Cliente Teste')
        category = Category.objects.create(name='Cat Teste')
        cls.item = Item.objects.create(name='Item Teste', price=100, quantity=20, category=category)
        cls.sale = Sale.objects.create(customer=cls.customer, grand_total=100)

    def test_sale_list_view_requires_login(self):
        """Verifica se a lista de vendas redireciona se o usuário não estiver logado."""
        response = self.client.get(reverse('saleslist'))
        self.assertRedirects(response, f"{reverse('user-login')}?next={reverse('saleslist')}")

    def test_sale_list_view_loads_correctly(self):
        """Verifica se a lista de vendas carrega para um usuário logado."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('saleslist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/sales_list.html')

    def test_sale_create_view_post_success(self):
        """Verifica se a view de criação de venda (AJAX) funciona com dados válidos."""
        self.client.login(username='testuser', password='password123')
        initial_item_quantity = self.item.quantity
        
        sale_data = {
            'customer': self.customer.pk,
            'sub_total': 200, 'grand_total': 200,
            'amount_paid': 200, 'amount_change': 0,
            'items': [{'id': self.item.pk, 'price': 100, 'quantity': 2, 'total_item': 200}]
        }
        
        response = self.client.post(
            reverse('sale-create'),
            data=json.dumps(sale_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, initial_item_quantity - 2)

    def test_sale_create_view_post_insufficient_stock(self):
        """Verifica se a venda falha se não houver estoque suficiente."""
        self.client.login(username='testuser', password='password123')
        
        sale_data = {
            'customer': self.customer.pk, 'sub_total': 20000, 'grand_total': 20000,
            'amount_paid': 20000, 'amount_change': 0,
            'items': [{'id': self.item.pk, 'price': 100, 'quantity': 99, 'total_item': 9900}]
        }
        
        response = self.client.post(
            reverse('sale-create'), data=json.dumps(sale_data), content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not enough stock', response.json()['message'])

    def test_sale_delete_view_permission_denied_for_normal_user(self):
        """Verifica se um usuário normal não pode deletar uma venda."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('sale-delete', args=[self.sale.pk]))
        self.assertEqual(response.status_code, 403)


class PurchaseViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        cls.vendor = Vendor.objects.create(name="Fornecedor Teste")
        category = Category.objects.create(name='Cat Teste')
        cls.item = Item.objects.create(name='Item Teste', price=100, quantity=20, category=category)
        cls.purchase = Purchase.objects.create(item=cls.item, vendor=cls.vendor, quantity=5, price=100)

    def test_purchase_list_view_loads_correctly(self):
        """Verifica se a lista de compras carrega."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('purchaseslist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/purchases_list.html')

    def test_purchase_delete_view_by_superuser(self):
        """Verifica se um superusuário pode deletar uma compra."""
        self.client.login(username='superuser', password='password123')
        initial_count = Purchase.objects.count()
        response = self.client.post(reverse('purchase-delete', args=[self.purchase.pk]))
        self.assertEqual(Purchase.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('purchaseslist'))


class ExportViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # --- CORRECTION APPLIED HERE ---
        customer = Customer.objects.create(
            first_name='Cliente Export', 
            phone='11999998888' # Add a phone number
        )
        Sale.objects.create(customer=customer, grand_total=500)

    def test_export_sales_to_excel_view(self):
        """Verifica a exportação de vendas para Excel."""
        response = self.client.get(reverse('sales-export'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        workbook = load_workbook(filename=BytesIO(response.content))
        worksheet = workbook.active
        self.assertEqual(worksheet['A1'].value, 'ID')
        # The assertion now expects the phone number we provided
        self.assertEqual(worksheet['C2'].value, '11999998888')
        self.assertEqual(worksheet.max_row, 2)