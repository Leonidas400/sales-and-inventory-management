# bills/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    BillListView,
    BillCreateView,
    BillUpdateView,
    BillDeleteView
)

class BillUrlsTest(SimpleTestCase):
    """Test suite for the URLs in the bills app."""

    def test_bill_list_url_is_resolved(self):
        """Verifica se a URL da lista de contas resolve para a view correta."""
        url = reverse('bill_list')  # Gera a URL a partir do nome 'bill_list'
        self.assertEqual(resolve(url).func.view_class, BillListView)

    def test_bill_create_url_is_resolved(self):
        """Verifica se a URL de criação de conta resolve para a view correta."""
        url = reverse('bill_create')
        self.assertEqual(resolve(url).func.view_class, BillCreateView)

    def test_bill_update_url_is_resolved(self):
        """Verifica se a URL de atualização de conta resolve para a view correta."""
        # Para URLs com parâmetros, passamos um argumento de exemplo.
        url = reverse('bill_update', args=['um-slug-qualquer'])
        self.assertEqual(resolve(url).func.view_class, BillUpdateView)

    def test_bill_delete_url_is_resolved(self):
        """Verifica se a URL de exclusão de conta resolve para a view correta."""
        # O mesmo vale para URLs com ID (pk).
        url = reverse('bill_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, BillDeleteView)