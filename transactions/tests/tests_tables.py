from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Sale, Purchase
from ..tables import SaleTable, PurchaseTable
from store.models import Item, Category
from accounts.models import Customer, Vendor, Profile

class SaleTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Cria os objetos necessários para testar a SaleTable."""
        customer = Customer.objects.create(first_name='Cliente Venda')
        
        # Cria a venda usando apenas os campos que o modelo Sale realmente possui
        Sale.objects.create(
            customer=customer,
            sub_total=100.00,
            grand_total=120.00
        )

    def test_sale_table_instantiation_and_row_count(self):
        """Verifica se a SaleTable é instanciada e tem o número correto de linhas."""
        table = SaleTable(Sale.objects.all())
        self.assertEqual(len(table.rows), 1)

    def test_sale_table_has_correct_columns(self):
        """Verifica se a SaleTable tem as colunas corretas."""
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
        """Cria os objetos necessários para testar a PurchaseTable."""
        vendor = Vendor.objects.create(name='Fornecedor Compra')
        category = Category.objects.create(name='Cat Compras')
        item = Item.objects.create(name='Item Compra', price=100, quantity=10, category=category)

        Purchase.objects.create(
            item=item,
            vendor=vendor,
            quantity=5,
            price=100.0
        )

    def test_purchase_table_instantiation_and_row_count(self):
        """Verifica se a PurchaseTable é instanciada e tem o número correto de linhas."""
        table = PurchaseTable(Purchase.objects.all())
        self.assertEqual(len(table.rows), 1)

    def test_purchase_table_has_correct_columns(self):
        """Verifica se a PurchaseTable tem as colunas corretas."""
        table = PurchaseTable(Purchase.objects.none())
        expected_columns = [
            'item', 'vendor', 'order_date', 'delivery_date', 'quantity',
            'delivery_status', 'price', 'total_value'
        ]
        rendered_column_names = [col.name for col in table.columns]
        self.assertEqual(rendered_column_names, expected_columns)