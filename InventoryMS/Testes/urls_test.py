#Falhou em 5 dos 8 testes
import os
import django
import unittest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryMS.settings')
django.setup()

from django.urls import resolve
from django.contrib import admin
import InventoryMS.urls as project_urls


class UrlsTest(unittest.TestCase):

    def test_urlpatterns_exists(self):
        self.assertTrue(hasattr(project_urls, 'urlpatterns'))
        self.assertIsInstance(project_urls.urlpatterns, (list, tuple))

    def test_admin_url(self):
        resolver = resolve('/admin/')
        self.assertEqual(resolver.func.__module__, admin.site.__class__.__module__)

    def _assert_resolves_to_namespace_or_app_name(self, path, expected_names):
        try:
            resolver = resolve(path)
        except Exception as e:
            self.fail(f"URL '{path}' could not be resolved: {e}")
        # Verifica namespace ou app_name, aceita qualquer string que contenha o esperado
        actual = resolver.namespace or resolver.app_name or ''
        self.assertTrue(any(expected in actual for expected in expected_names),
                        f"URL '{path}' resolved to namespace/app_name '{actual}', expected one of {expected_names}")

    def test_store_root_url_resolves(self):
        # Se 'store' não usa namespace, pode esperar nome vazio também
        self._assert_resolves_to_namespace_or_app_name('/', ['store', ''])

    def test_staff_url_resolves(self):
        self._assert_resolves_to_namespace_or_app_name('/staff/', ['accounts'])

    def test_transactions_url_resolves(self):
        self._assert_resolves_to_namespace_or_app_name('/transactions/', ['transactions'])

    def test_accounts_url_resolves(self):
        self._assert_resolves_to_namespace_or_app_name('/accounts/', ['accounts'])

    def test_invoice_url_resolves(self):
        self._assert_resolves_to_namespace_or_app_name('/invoice/', ['invoice'])

    def test_bills_url_resolves(self):
        self._assert_resolves_to_namespace_or_app_name('/bills/', ['bills'])


if __name__ == '__main__':
    unittest.main()
