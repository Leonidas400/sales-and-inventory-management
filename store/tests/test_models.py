import os
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Category, Vendor, Item, Delivery

class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.assertEqual(category.name, 'Bebidas')
        self.assertEqual(category.slug, 'bebidas')

class VendorModelTest(TestCase):

    def test_create_vendor(self):
        vendor_name = os.environ.get('TEST_VENDOR_NAME', 'Fornecedor A')
        vendor = Vendor.objects.create(name=vendor_name)
        self.assertEqual(str(vendor), vendor_name)

class ItemModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Bebidas', slug='bebidas')
        self.vendor = Vendor.objects.create(name='Fornecedor A')

    def test_create_item(self):
        item_name = os.environ.get('TEST_ITEM_NAME', 'Suco de Laranja')
        expiring_date = timezone.now() + datetime.timedelta(days=10)
        
        item = Item.objects.create(
            name=item_name,
            description='Suco natural',
            category=self.category,
            quantity=10,
            price=4.5,
            expiring_date=expiring_date,
            vendor=self.vendor,
        )
        
        self.assertIn(item_name, str(item))
        self.assertIn(self.category.name, str(item))
        
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
        
        customer_name = os.environ.get('TEST_CUSTOMER_NAME', 'Matheus José')
        phone_number = os.environ.get('TEST_PHONE_NUMBER', '+5511929697838')
        location = os.environ.get('TEST_LOCATION', 'Rua Coutinho, 13')
        date = timezone.now() + datetime.timedelta(days=1)
        
        delivery = Delivery.objects.create(
            item=self.item,
            customer_name=customer_name,
            phone_number=phone_number,
            location=location,
            date=date,
            is_delivered=False
        )
        
        
        self.assertIn(self.item.name, str(delivery))
        self.assertIn(customer_name, str(delivery))
        self.assertIn(location, str(delivery))
        
        self.assertEqual(delivery.customer_name, customer_name)
        self.assertEqual(delivery.location, location)
        self.assertFalse(delivery.is_delivered)