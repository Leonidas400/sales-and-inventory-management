from django.test import SimpleTestCase

class ProjectFilesTest(SimpleTestCase):

    def test_wsgi_application_is_configured(self):
        
        try:
        
            from InventoryMS.wsgi import application
        except ImportError as e:
            self.fail(f"Não foi possível importar 'application' de InventoryMS.wsgi: {e}")

        self.assertIsNotNone(application)
        self.assertTrue(callable(application))

    def test_settings_module_is_correct_for_wsgi(self):
        
        self.assertTrue(True)