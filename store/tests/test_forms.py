#Passou nos 6 testes

from django.test import TestCase
from django.utils import timezone
from store.forms import ItemForm, CategoryForm, DeliveryForm
from store.models import Category, Vendor, Item
import datetime

class ItemFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.vendor = Vendor.objects.create(name='Fornecedor A')

    def test_valid_form(self):
        form_data = {
            'name': 'Suco de Laranja',
            'description': 'Delicioso suco natural',
            'category': self.category.id,
            'quantity': 10,
            'price': 4.99,
            # Passando datetime "aware" formatado para widget datetime-local
            'expiring_date': (timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%dT%H:%M'),
            'vendor': self.vendor.id,
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form_data = {
            'description': 'Delicioso suco natural',
            'category': self.category.id,
            'quantity': 10,
            'price': 4.99,
            'expiring_date': (timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%dT%H:%M'),
            'vendor': self.vendor.id,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class CategoryFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'Bebidas'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_name(self):
        form_data = {'name': ''}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class DeliveryFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.vendor = Vendor.objects.create(name='Fornecedor A')
        self.item = Item.objects.create(
            name='Suco de Laranja',
            description='Suco natural',
            category=self.category,
            quantity=10,
            price=4.5,
            expiring_date=timezone.now() + datetime.timedelta(days=10),
            vendor=self.vendor,
        )

    def test_valid_form(self):
        form_data = {
            'item': self.item.id,
            'customer_name': 'João Silva',
            'phone_number': '+5511999998888',  # Formato de telefone válido
            'location': 'Rua Exemplo, 123',
            'date': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'is_delivered': True,
        }
        form = DeliveryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_customer_name(self):
        form_data = {
            'item': self.item.id,
            'customer_name': '',
            'phone_number': '+5511999998888',
            'location': 'Rua Exemplo, 123',
            'date': (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'is_delivered': False,
        }
        form = DeliveryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('customer_name', form.errors)
