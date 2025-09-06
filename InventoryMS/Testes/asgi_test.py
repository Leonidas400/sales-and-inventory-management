#python -m unittest InventoryMS.Testes.asgi_test
import unittest

class TestASGI(unittest.TestCase):

    def test_asgi_application_import(self):
        import InventoryMS.asgi
        self.assertTrue(hasattr(InventoryMS.asgi, "application"))

if __name__ == "__main__":
    unittest.main()

    #Aprovado no teste

