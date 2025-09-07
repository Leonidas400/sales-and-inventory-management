#Passou nos 18 testes
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import (
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
        url = reverse('store:dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_products_list_url(self):
        url = reverse('store:productslist')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url(self):
        url = reverse('store:product-detail', kwargs={'slug': 'suco-de-laranja'})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_product_create_url(self):
        url = reverse('store:product-create')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_product_update_url(self):
        url = reverse('store:product-update', kwargs={'slug': 'suco-de-laranja'})
        self.assertEqual(resolve(url).func.view_class, ProductUpdateView)

    def test_product_delete_url(self):
        url = reverse('store:product-delete', kwargs={'slug': 'suco-de-laranja'})
        self.assertEqual(resolve(url).func.view_class, ProductDeleteView)

    def test_item_search_url(self):
        url = reverse('store:item_search_list_view')
        self.assertEqual(resolve(url).func.view_class, ItemSearchListView)

    def test_deliveries_list_url(self):
        url = reverse('store:deliveries')
        self.assertEqual(resolve(url).func.view_class, DeliveryListView)

    def test_delivery_detail_url(self):
        url = reverse('store:delivery-detail', kwargs={'slug': 'suco-de-laranja'})
        self.assertEqual(resolve(url).func.view_class, DeliveryDetailView)

    def test_delivery_create_url(self):
        url = reverse('store:delivery-create')
        self.assertEqual(resolve(url).func.view_class, DeliveryCreateView)

    def test_delivery_update_url(self):
        url = reverse('store:delivery-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DeliveryUpdateView)

    def test_delivery_delete_url(self):
        url = reverse('store:delivery-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DeliveryDeleteView)

    def test_get_items_ajax_url(self):
        url = reverse('store:get_items')
        self.assertEqual(resolve(url).func, get_items_ajax_view)

    def test_categories_list_url(self):
        url = reverse('store:category-list')
        self.assertEqual(resolve(url).func.view_class, CategoryListView)

    def test_category_detail_url(self):
        url = reverse('store:category-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDetailView)

    def test_category_create_url(self):
        url = reverse('store:category-create')
        self.assertEqual(resolve(url).func.view_class, CategoryCreateView)

    def test_category_update_url(self):
        url = reverse('store:category-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryUpdateView)

    def test_category_delete_url(self):
        url = reverse('store:category-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDeleteView)
