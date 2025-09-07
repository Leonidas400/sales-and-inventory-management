from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Sale, Purchase
from ..tables import SaleTable, PurchaseTable
from store.models import Item, Category
from accounts.models import Customer, Vendor, Profile

class SaleTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        customer = Customer.objects.create(first_name='Cliente Novo')
        
        Sale.objects.create(
            customer=customer,
            sub_total=100.00,
            grand_total=120.00
        )

    def test_sale_table_instantiation_and_row_count(self):
        table = SaleTable(Sale.objects.all())
        self.assertEqual(len(table.rows), 1)

    def test_sale_table_has_correct_columns(self):
        table = SaleTable(Sale.objects.none())
        expected_columns = [
            'item', 'customer_name', 'transaction_date', 'payment_method',
            'quantity', 'price', 'total_value', 'amount_received',
            'balance', 'profile'
        ]
        rendered_column_names = [col.name for col in table.columns]
        self.assertEqual(rendered_column_names, expected_columns)


class PurchaseTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        vendor = Vendor.objects.create(name='Fornecedor Roberto')
        category = Category.objects.create(name='Categoria Compras')
        item = Item.objects.create(name='Item Para Compra', price=100, quantity=10, category=category)

        Purchase.objects.create(
            item=item,
            vendor=vendor,
            quantity=5,
            price=100.0
        )

    def test_purchase_table_instantiation_and_row_count(self):
        table = PurchaseTable(Purchase.objects.all())
        self.assertEqual(len(table.rows), 1)

    def test_purchase_table_has_correct_columns(self):
        table = PurchaseTable(Purchase.objects.none())
        expected_columns = [
            'item', 'vendor', 'order_date', 'delivery_date', 'quantity',
            'delivery_status', 'price', 'total_value'
        ]
        rendered_column_names = [col.name for col in table.columns]
        self.assertEqual(rendered_column_names, expected_columns)