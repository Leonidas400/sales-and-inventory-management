#Passou nos 3 testes
import unittest
import os
import InventoryMS.wsgi as wsgi  # Importa o módulo wsgi.py do projeto

class WsgiTest(unittest.TestCase):

    def test_application_defined(self):
        self.assertTrue(hasattr(wsgi, 'application'))

    def test_application_callable(self):
        self.assertTrue(callable(wsgi.application))

    def test_django_settings_module_env(self):
        self.assertEqual(os.environ.get('DJANGO_SETTINGS_MODULE'), 'InventoryMS.settings')

if __name__ == '__main__':
    unittest.main()