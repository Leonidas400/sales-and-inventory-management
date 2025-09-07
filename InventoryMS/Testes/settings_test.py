#Aprovado nos 12 testes
import unittest
from django.conf import settings
import os

class SettingsTest(unittest.TestCase):

    def test_secret_key_set(self):
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, "")

    def test_debug_false_on_production(self):
        if os.environ.get('ENVIRONMENT') == 'production':
            self.assertFalse(settings.DEBUG)

    def test_installed_apps_contains_store(self):
        self.assertTrue(any(app.startswith('store') for app in settings.INSTALLED_APPS))

    def test_database_engine(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_allowed_hosts_is_list(self):
        self.assertIsInstance(settings.ALLOWED_HOSTS, (list, tuple))

    def test_middleware_not_empty(self):
        self.assertGreater(len(settings.MIDDLEWARE), 0)

    def test_root_urlconf_string(self):
        self.assertIsInstance(settings.ROOT_URLCONF, str)
        self.assertTrue(settings.ROOT_URLCONF.endswith('.urls'))

    def test_templates_configured(self):
        self.assertIsInstance(settings.TEMPLATES, list)
        self.assertGreater(len(settings.TEMPLATES), 0)
        for tpl in settings.TEMPLATES:
            self.assertIn('BACKEND', tpl)
            self.assertIn('OPTIONS', tpl)

    def test_static_and_media_urls(self):
        self.assertTrue(settings.STATIC_URL.startswith('/'))
        self.assertTrue(settings.MEDIA_URL.startswith('/'))

    def test_password_validators_configured(self):
        self.assertIsInstance(settings.AUTH_PASSWORD_VALIDATORS, list)
        self.assertGreater(len(settings.AUTH_PASSWORD_VALIDATORS), 0)

    def test_language_code_and_timezone(self):
        self.assertIsInstance(settings.LANGUAGE_CODE, str)
        self.assertGreater(len(settings.LANGUAGE_CODE), 0)
        self.assertIsInstance(settings.TIME_ZONE, str)
        self.assertGreater(len(settings.TIME_ZONE), 0)

    def test_default_auto_field(self):
        self.assertEqual(settings.DEFAULT_AUTO_FIELD, 'django.db.models.BigAutoField')


if __name__ == '__main__':
    unittest.main()
