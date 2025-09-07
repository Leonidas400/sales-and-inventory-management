#Passou nos 3 testes
from django.test import TestCase
from store.tables import ItemTable, DeliveryTable
from store.models import Item, Delivery, Category, Vendor
import datetime

class ItemTableTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Bebidas', slug='bebidas')
        vendor = Vendor.objects.create(name='Fornecedor A')
        self.item = Item.objects.create(
            name='Suco de Laranja',
            category=category,
            quantity=10,
            price=5.0,
            expiring_date=datetime.date.today() + datetime.timedelta(days=10),
            vendor=vendor
        )
        self.table = ItemTable([self.item])

    def test_table_fields(self):
        expected_fields = ('id', 'name', 'category', 'quantity', 'selling_price', 'expiring_date', 'vendor')
        self.assertEqual(tuple(self.table.base_columns.keys()), expected_fields)

    def test_table_template(self):
        self.assertEqual(self.table.template_name, "django_tables2/semantic.html")

class DeliveryTableTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Bebidas', slug='bebidas')
        vendor = Vendor.objects.create(name='Fornecedor A')
        item = Item.objects.create(
            name='Suco de Laranja',
            category=category,
            quantity=10,
            price=5.0,
            expiring_date=datetime.date.today() + datetime.timedelta(days=10),
            vendor=vendor
        )
        self.delivery = Delivery.objects.create(
            item=item,
            customer_name='Matheus José',
            phone_number='123456789',
            location='Rua tal tal tal',
            date=datetime.date.today(),
            is_delivered=False
        )
        self.table = DeliveryTable([self.delivery])

    def test_table_fields(self):
        expected_fields = ('id', 'item', 'customer_name', 'phone_number', 'location', 'date', 'is_delivered')
        self.assertEqual(tuple(self.table.base_columns.keys()), expected_fields)
