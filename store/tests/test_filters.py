#Passou nos 3 testes
from django.test import TestCase
from store.models import Item, Category, Vendor
from store.filters import ProductFilter

class ProductFilterTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name='Bebidas', slug='bebidas')
        self.category2 = Category.objects.create(name='Comidas', slug='comidas')
        self.vendor1 = Vendor.objects.create(name='Fornecedor A')
        self.vendor2 = Vendor.objects.create(name='Fornecedor B')

        self.item1 = Item.objects.create(name='Suco de Laranja', category=self.category1, vendor=self.vendor1, quantity=10, price=5)
        self.item2 = Item.objects.create(name='Pão', category=self.category2, vendor=self.vendor2, quantity=20, price=2)

    def test_filter_by_name(self):
        f = ProductFilter({'name': 'Suco'}, queryset=Item.objects.all())
        self.assertIn(self.item1, f.qs)
        self.assertNotIn(self.item2, f.qs)

    def test_filter_by_category(self):
        f = ProductFilter({'category': self.category1.id}, queryset=Item.objects.all())
        self.assertIn(self.item1, f.qs)
        self.assertNotIn(self.item2, f.qs)

    def test_filter_by_vendor(self):
        f = ProductFilter({'vendor': self.vendor2.id}, queryset=Item.objects.all())
        self.assertIn(self.item2, f.qs)
        self.assertNotIn(self.item1, f.qs)