from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    BillListView,
    BillCreateView,
    BillUpdateView,
    BillDeleteView
)

class BillUrlsTest(SimpleTestCase):

    def test_bill_list_url_is_resolved(self):
        url = reverse('bill_list')
        self.assertEqual(resolve(url).func.view_class, BillListView)

    def test_bill_create_url_is_resolved(self):
        url = reverse('bill_create')
        self.assertEqual(resolve(url).func.view_class, BillCreateView)

    def test_bill_update_url_is_resolved(self):
        url = reverse('bill_update', args=['um-slug-qualquer'])
        self.assertEqual(resolve(url).func.view_class, BillUpdateView)

    def test_bill_delete_url_is_resolved(self):
        url = reverse('bill_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, BillDeleteView)