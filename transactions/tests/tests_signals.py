from django.test import TestCase
from decimal import Decimal
from ..models import Purchase
from accounts.models import Vendor
from store.models import Item, Category

class TransactionSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.vendor = Vendor.objects.create(name='Fornecedor Sinal')
        category = Category.objects.create(name='Categoria Sinal')
        cls.item = Item.objects.create(
            name='Produto Makita', 
            price=50.0, 
            category=category, 
            quantity=10
        )

    def test_update_item_quantity_signal_on_purchase_creation(self):
        initial_item_quantity = self.item.quantity
        purchase_quantity = 5

        Purchase.objects.create(
            item=self.item,
            vendor=self.vendor,
            quantity=purchase_quantity,
            price=Decimal('50.00')
        )

        self.item.refresh_from_db()

        expected_quantity = initial_item_quantity + purchase_quantity
        self.assertEqual(self.item.quantity, expected_quantity)