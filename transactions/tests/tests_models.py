from django.test import TestCase
from decimal import Decimal
from ..models import Sale, SaleDetail, Purchase
from accounts.models import Customer, Vendor
from store.models import Item, Category

class SaleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(first_name='Jorge', last_name='Torresmo')
        category = Category.objects.create(name='Categoria Teste')
        cls.item1 = Item.objects.create(name='Produto Makita', price=10.0, category=category)
        cls.item2 = Item.objects.create(name='Produto Pasta', price=20.0, category=category)
        
        cls.sale = Sale.objects.create(customer=cls.customer, grand_total=100)
        SaleDetail.objects.create(sale=cls.sale, item=cls.item1, quantity=3, price=10.0, total_detail=30.0)
        SaleDetail.objects.create(sale=cls.sale, item=cls.item2, quantity=2, price=20.0, total_detail=40.0)

    def test_sale_creation(self):
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(self.sale.customer.first_name, 'Jorge')

    def test_sum_products_method(self):
        total_quantity = self.sale.sum_products()
        self.assertEqual(total_quantity, 5)


class PurchaseModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.vendor = Vendor.objects.create(name='Fornecedor Google')
        category = Category.objects.create(name='Categoria Teste')
        cls.item = Item.objects.create(name='Produto Comprado', price=50.0, category=category, quantity=10)

    def test_purchase_save_method(self):
        initial_item_quantity = self.item.quantity

        purchase = Purchase(
            item=self.item,
            vendor=self.vendor,
            quantity=5,
            price=Decimal('50.00')
        )
        purchase.save()

        self.assertEqual(purchase.total_value, Decimal('250.00'))

        self.item.refresh_from_db()

        self.assertEqual(self.item.quantity, initial_item_quantity + 5)

    def test_purchase_defaults(self):
        purchase = Purchase.objects.create(
            item=self.item,
            vendor=self.vendor,
            quantity=1,
            price=Decimal('10.00')
        )
        self.assertEqual(purchase.delivery_status, 'P')