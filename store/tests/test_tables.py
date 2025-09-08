import os
import datetime
from django.test import TestCase
from django.utils import timezone 
from ..tables import ItemTable, DeliveryTable
from ..models import Item, Delivery, Category, Vendor

class ItemTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Bebidas', slug='bebidas')
        vendor = Vendor.objects.create(name='Fornecedor A')
        cls.item = Item.objects.create(
            name='Suco de Laranja',
            category=category,
            quantity=10,
            price=5.0,
            expiring_date=timezone.now().date() + datetime.timedelta(days=10),
            vendor=vendor
        )
        cls.table = ItemTable(Item.objects.all())

    def test_table_fields(self):
        expected_fields = ('id', 'name', 'category', 'quantity', 'selling_price', 'expiring_date', 'vendor')
        self.assertEqual(tuple(self.table.base_columns.keys()), expected_fields)

    def test_table_template(self):
        self.assertEqual(self.table.template_name, "django_tables2/semantic.html")

class DeliveryTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        customer_name = os.environ.get('TEST_CUSTOMER_NAME', 'Matheus José')
        phone_number = os.environ.get('TEST_PHONE_NUMBER', '11929697838')
        location = os.environ.get('TEST_LOCATION', 'Rua Coutinho, 13')

        category = Category.objects.create(name='Bebidas', slug='bebidas')
        vendor = Vendor.objects.create(name='Fornecedor A')
        item = Item.objects.create(
            name='Suco de Laranja',
            category=category,
            quantity=10,
            price=5.0,
            expiring_date=timezone.now().date() + datetime.timedelta(days=10),
            vendor=vendor
        )
        cls.delivery = Delivery.objects.create(
            item=item,
            customer_name=customer_name,
            phone_number=phone_number,
            location=location,
            date=timezone.now().date(),
            is_delivered=False
        )
        cls.table = DeliveryTable(Delivery.objects.all())

    def test_table_fields(self):
        expected_fields = ('id', 'item', 'customer_name', 'phone_number', 'location', 'date', 'is_delivered')
        self.assertEqual(tuple(self.table.base_columns.keys()), expected_fields)