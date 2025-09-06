from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    InvoiceListView,
    InvoiceDetailView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView
)

class InvoiceUrlsTest(SimpleTestCase):

    def test_invoice_list_url_resolves(self):
        url = reverse('invoicelist')
        self.assertEqual(url, '/invoice/invoices/')
        self.assertEqual(resolve(url).func.view_class, InvoiceListView)

    def test_invoice_detail_url_resolves(self):
        url = reverse('invoice-detail', args=['a-sample-slug'])
        self.assertEqual(url, '/invoice/invoice/a-sample-slug/')
        self.assertEqual(resolve(url).func.view_class, InvoiceDetailView)

    def test_invoice_create_url_resolves(self):
        url = reverse('invoice-create')
        self.assertEqual(url, '/invoice/new-invoice/')
        self.assertEqual(resolve(url).func.view_class, InvoiceCreateView)

    def test_invoice_update_url_resolves(self):
        url = reverse('invoice-update', args=['a-sample-slug'])
        self.assertEqual(url, '/invoice/invoice/a-sample-slug/update/')
        self.assertEqual(resolve(url).func.view_class, InvoiceUpdateView)

    def test_invoice_delete_url_resolves(self):
        url = reverse('invoice-delete', args=[1])
        self.assertEqual(url, '/invoice/invoice/1/delete/')
        self.assertEqual(resolve(url).func.view_class, InvoiceDeleteView)