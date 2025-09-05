# transactions/tests/test_models.py

from django.test import TestCase
from decimal import Decimal
from ..models import Sale, SaleDetail, Purchase
from accounts.models import Customer, Vendor
from store.models import Item, Category

class SaleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Cria objetos dependentes para o teste de Sale
        cls.customer = Customer.objects.create(first_name='Cliente', last_name='Teste')
        category = Category.objects.create(name='Categoria Teste')
        cls.item1 = Item.objects.create(name='Produto A', price=10.0, category=category)
        cls.item2 = Item.objects.create(name='Produto B', price=20.0, category=category)
        
        # Cria a venda e os detalhes da venda
        cls.sale = Sale.objects.create(customer=cls.customer, grand_total=100)
        SaleDetail.objects.create(sale=cls.sale, item=cls.item1, quantity=3, price=10.0, total_detail=30.0)
        SaleDetail.objects.create(sale=cls.sale, item=cls.item2, quantity=2, price=20.0, total_detail=40.0)

    def test_sale_creation(self):
        """Verifica se a venda foi criada corretamente."""
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(self.sale.customer.first_name, 'Cliente')

    def test_sum_products_method(self):
        """Verifica se o método sum_products() calcula a quantidade total de itens."""
        # A venda tem 3 unidades do item1 e 2 do item2
        total_quantity = self.sale.sum_products()
        self.assertEqual(total_quantity, 5)


class PurchaseModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Cria objetos dependentes para o teste de Purchase
        cls.vendor = Vendor.objects.create(name='Fornecedor Teste')
        category = Category.objects.create(name='Categoria Teste')
        # Cria um item com quantidade inicial para testar a atualização de estoque
        cls.item = Item.objects.create(name='Produto Comprado', price=50.0, category=category, quantity=10)

    def test_purchase_save_method(self):
        """
        Verifica se o método save() calcula o 'total_value' e atualiza o estoque do item.
        """
        initial_item_quantity = self.item.quantity

        # Cria a compra, mas não salva ainda
        purchase = Purchase(
            item=self.item,
            vendor=self.vendor,
            quantity=5,
            price=Decimal('50.00')
        )
        # Salva o objeto, o que dispara a lógica customizada
        purchase.save()

        # Verifica se o total_value foi calculado corretamente
        self.assertEqual(purchase.total_value, Decimal('250.00')) # 5 * 50.00

        # Pega o item atualizado do banco de dados
        self.item.refresh_from_db()

        # Verifica se a quantidade do item foi incrementada corretamente
        self.assertEqual(self.item.quantity, initial_item_quantity + 5)

    def test_purchase_defaults(self):
        """Verifica os valores padrão do modelo Purchase."""
        purchase = Purchase.objects.create(
            item=self.item,
            vendor=self.vendor,
            quantity=1,
            price=Decimal('10.00')
        )
        self.assertEqual(purchase.delivery_status, 'P') # Verifica o status padrão