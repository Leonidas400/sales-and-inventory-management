# transactions/tests/test_signals.py

from django.test import TestCase
from decimal import Decimal
from ..models import Purchase
from accounts.models import Vendor
from store.models import Item, Category

class TransactionSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Cria os objetos necessários para o teste do signal."""
        cls.vendor = Vendor.objects.create(name='Fornecedor Sinal')
        category = Category.objects.create(name='Categoria Sinal')
        # Cria um item com uma quantidade inicial de estoque
        cls.item = Item.objects.create(
            name='Produto Sinal', 
            price=50.0, 
            category=category, 
            quantity=10
        )

    def test_update_item_quantity_signal_on_purchase_creation(self):
        """
        Verifica se o signal 'update_item_quantity' incrementa a quantidade
        do item quando uma nova compra é criada.
        """
        initial_item_quantity = self.item.quantity
        purchase_quantity = 5

        # Cria uma nova compra, o que deve disparar o signal
        Purchase.objects.create(
            item=self.item,
            vendor=self.vendor,
            quantity=purchase_quantity,
            price=Decimal('50.00')
        )

        # Pega o item atualizado do banco de dados para garantir que estamos
        # vendo o dado mais recente
        self.item.refresh_from_db()

        # Verifica se a quantidade do item foi incrementada corretamente
        expected_quantity = initial_item_quantity + purchase_quantity
        self.assertEqual(self.item.quantity, expected_quantity)