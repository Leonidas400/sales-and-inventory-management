import os
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    dashboard,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ItemSearchListView,
    DeliveryListView,
    DeliveryDetailView,
    DeliveryCreateView,
    DeliveryUpdateView,
    DeliveryDeleteView,
    get_items_ajax_view,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

class StoreUrlsTest(SimpleTestCase):

    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_products_list_url(self):
        url = reverse('productslist')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url(self):
        test_slug = os.environ.get('TEST_SLUG', 'sample-slug')
        url = reverse('product-detail', kwargs={'slug': test_slug})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_product_create_url(self):
        url = reverse('product-create')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_product_update_url(self):
        test_slug = os.environ.get('TEST_SLUG', 'sample-slug')
        url = reverse('product-update', kwargs={'slug': test_slug})
        self.assertEqual(resolve(url).func.view_class, ProductUpdateView)

    def test_product_delete_url(self):
        test_slug = os.environ.get('TEST_SLUG', 'sample-slug')
        url = reverse('product-delete', kwargs={'slug': test_slug})
        self.assertEqual(resolve(url).func.view_class, ProductDeleteView)

    def test_item_search_url(self):
        url = reverse('item_search_list_view')
        self.assertEqual(resolve(url).func.view_class, ItemSearchListView)

    def test_deliveries_list_url(self):
        url = reverse('deliveries')
        self.assertEqual(resolve(url).func.view_class, DeliveryListView)

    def test_delivery_detail_url(self):
        test_slug = os.environ.get('TEST_SLUG', 'sample-slug')
        url = reverse('delivery-detail', kwargs={'slug': test_slug})
        self.assertEqual(resolve(url).func.view_class, DeliveryDetailView)

    def test_delivery_create_url(self):
        url = reverse('delivery-create')
        self.assertEqual(resolve(url).func.view_class, DeliveryCreateView)

    def test_delivery_update_url(self):
        url = reverse('delivery-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DeliveryUpdateView)

    def test_delivery_delete_url(self):
        url = reverse('delivery-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DeliveryDeleteView)

    def test_get_items_ajax_url(self):
        url = reverse('get_items')
        self.assertEqual(resolve(url).func, get_items_ajax_view)

    def test_categories_list_url(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).func.view_class, CategoryListView)

    def test_category_detail_url(self):
        url = reverse('category-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDetailView)

    def test_category_create_url(self):
        url = reverse('category-create')
        self.assertEqual(resolve(url).func.view_class, CategoryCreateView)

    def test_category_update_url(self):
        url = reverse('category-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryUpdateView)

    def test_category_delete_url(self):
        url = reverse('category-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDeleteView)
