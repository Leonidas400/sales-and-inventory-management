#passou nos 4 testes
from django.test import TestCase
from django.utils import timezone
from store.models import Category, Vendor, Item, Delivery
import datetime

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.assertEqual(str(category), 'Category: Bebidas')
        self.assertEqual(category.slug, 'bebidas')

class VendorModelTest(TestCase):
    def test_create_vendor(self):
        vendor = Vendor.objects.create(name='Fornecedor A')
        self.assertEqual(str(vendor), 'Fornecedor A')  # Ajuste conforme seu __str__

class ItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.vendor = Vendor.objects.create(name='Fornecedor A')

    def test_create_item(self):
        expiring_date = timezone.now() + datetime.timedelta(days=10)
        item = Item.objects.create(
            name='Suco de Laranja',
            description='Suco natural',
            category=self.category,
            quantity=10,
            price=4.5,
            expiring_date=expiring_date,
            vendor=self.vendor,
        )
        self.assertEqual(str(item), 'Suco de Laranja - Category: Category: Bebidas, Quantity: 10')
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.vendor, self.vendor)
        self.assertEqual(item.price, 4.5)

class DeliveryModelTest(TestCase):
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

    def test_create_delivery(self):
        date = timezone.now() + datetime.timedelta(days=1)
        delivery = Delivery.objects.create(
            item=self.item,
            customer_name='Matheus José',
            phone_number='+5511999998888',
            location='Rua tal tal tal',
            date=date,
            is_delivered=False
        )
        self.assertEqual(str(delivery), f'Delivery of {self.item} to Matheus José at Rua tal tal tal on {date}')
        self.assertEqual(delivery.customer_name, 'Matheus José')
        self.assertEqual(delivery.location, 'Rua tal tal tal')
        self.assertFalse(delivery.is_delivered)
