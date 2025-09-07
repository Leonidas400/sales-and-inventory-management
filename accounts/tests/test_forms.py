from django.test import TestCase
from ..forms import VendorForm

class VendorFormTest(TestCase):

    def test_vendor_form_valid_data(self):
        form_data = {
            'name': 'Fornecedor Jorge',
            'phone_number': '11966694331',
            'address': 'Rua dos Amores, 149'
        }
        form = VendorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vendor_form_no_data(self):
        form = VendorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('name', form.errors)

    def test_vendor_form_missing_name(self):
        form_data = {
            'phone_number': '11966694331',
            'address': 'Rua dos Amores, 149'
        }
        form = VendorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())