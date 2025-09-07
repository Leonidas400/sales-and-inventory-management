from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    PurchaseListView,
    PurchaseDetailView,
    PurchaseCreateView,
    PurchaseUpdateView,
    PurchaseDeleteView,
    SaleListView,
    SaleDetailView,
    sale_create_view,
    SaleDeleteView,
    export_sales_to_excel,
    export_purchases_to_excel
)

class TransactionUrlsTest(SimpleTestCase):

    def test_purchase_list_url_resolves(self):
        url = reverse('purchaseslist')
        self.assertEqual(url, '/transactions/purchases/')
        self.assertEqual(resolve(url).func.view_class, PurchaseListView)

    def test_purchase_create_url_resolves(self):
        url = reverse('purchase-create')
        self.assertEqual(url, '/transactions/new-purchase/')
        self.assertEqual(resolve(url).func.view_class, PurchaseCreateView)

    def test_purchase_update_url_resolves(self):
        url = reverse('purchase-update', args=[1])
        self.assertEqual(url, '/transactions/purchase/1/update/')
        self.assertEqual(resolve(url).func.view_class, PurchaseUpdateView)

    def test_sale_list_url_resolves(self):
        url = reverse('saleslist')
        self.assertEqual(url, '/transactions/sales/')
        self.assertEqual(resolve(url).func.view_class, SaleListView)

    def test_sale_create_url_resolves(self):
        url = reverse('sale-create')
        self.assertEqual(url, '/transactions/new-sale/')
        self.assertEqual(resolve(url).func, sale_create_view)

    def test_sales_export_url_resolves(self):
        url = reverse('sales-export')
        self.assertEqual(url, '/transactions/sales/export/')
        self.assertEqual(resolve(url).func, export_sales_to_excel)