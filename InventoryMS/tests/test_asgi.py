from django.test import SimpleTestCase
from django.core.asgi import get_asgi_application

class ProjectFilesTest(SimpleTestCase):

    def test_asgi_application_is_configured(self):
        try:
            from InventoryMS.asgi import application
        except ImportError as e:
            self.fail(f"Não foi possível importar 'application' de InventoryMS.asgi: {e}")

        self.assertIsNotNone(application)
        self.assertTrue(callable(application))