import os
from django.test import SimpleTestCase
from django.conf import settings

class SettingsTest(SimpleTestCase):


    def test_secret_key_is_set(self):
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, "")
        self.assertNotEqual(settings.SECRET_KEY, 'SECRET_KEY', "SECRET_KEY padrão não deve ser usada.")

    def test_debug_is_false_in_production(self):
        if os.environ.get('ENVIRONMENT') == 'production':
            self.assertFalse(settings.DEBUG, "DEBUG deve ser False em produção.")

    def test_required_apps_are_installed(self):
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'store.apps.StoreConfig',
            'accounts.apps.AccountsConfig',
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_database_engine_is_sqlite(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
    
    def test_root_urlconf_is_correct(self):
        self.assertEqual(settings.ROOT_URLCONF, 'InventoryMS.urls')

    def test_static_url_is_configured(self):
        self.assertEqual(settings.STATIC_URL, '/static/')