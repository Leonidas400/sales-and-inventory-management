from django.test import TestCase
from ..models import Item, Category, Vendor
from ..filters import ProductFilter

class ProductFilterTest(TestCase):

    def setUp(self):
        
        self.category1 = Category.objects.create(name='Bebidas', slug='bebidas')
        self.category2 = Category.objects.create(name='Comidas', slug='comidas')
        self.vendor1 = Vendor.objects.create(name='Fornecedor A')
        self.vendor2 = Vendor.objects.create(name='Fornecedor B')

        self.item1 = Item.objects.create(name='Suco de Laranja', category=self.category1, vendor=self.vendor1, quantity=10, price=5)
        self.item2 = Item.objects.create(name='Pão de Queijo', category=self.category2, vendor=self.vendor2, quantity=20, price=2)

    def test_filter_by_name(self):
        
        filter_data = {'name': 'Suco'}
        filtered_queryset = ProductFilter(filter_data, queryset=Item.objects.all()).qs

        self.assertIn(self.item1, filtered_queryset)
        self.assertNotIn(self.item2, filtered_queryset)

    def test_filter_by_category(self):
        
        filter_data = {'category': self.category1.id}
        filtered_queryset = ProductFilter(filter_data, queryset=Item.objects.all()).qs

        self.assertIn(self.item1, filtered_queryset)
        self.assertNotIn(self.item2, filtered_queryset)

    def test_filter_by_vendor(self):
    
        filter_data = {'vendor': self.vendor2.id}
        filtered_queryset = ProductFilter(filter_data, queryset=Item.objects.all()).qs

        self.assertIn(self.item2, filtered_queryset)
        self.assertNotIn(self.item1, filtered_queryset)