# accounts/tests/test_forms.py

from django.test import TestCase
from ..forms import VendorForm

class VendorFormTest(TestCase):
    """Test suite for the VendorForm."""

    def test_vendor_form_valid_data(self):
        """
        Testa se o formulário é válido quando preenchido com dados corretos.
        """
        form_data = {
            'name': 'Fornecedor Teste',
            'phone_number': '11987654321',
            'address': 'Rua dos Testes, 123'
        }
        form = VendorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vendor_form_no_data(self):
        """
        Testa se o formulário é inválido quando enviado vazio.
        """
        form = VendorForm(data={})
        self.assertFalse(form.is_valid())
        #Verifica se há erro em apenas 1 campo
        self.assertEqual(len(form.errors), 1)
        #Verifica se o erro é especificamente no campo 'name'
        self.assertIn('name', form.errors)

    def test_vendor_form_missing_name(self):
        """
        Testa se o formulário é inválido se o campo 'name' (obrigatório) estiver faltando.
        """
        form_data = {
            'phone_number': '11987654321',
            'address': 'Rua dos Testes, 123'
        }
        form = VendorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys()) # Verifica se o erro está no campo 'name'