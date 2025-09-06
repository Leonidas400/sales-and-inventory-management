from django.test import TestCase
from ..forms import PurchaseForm
from store.models import Item, Category
from accounts.models import Vendor
import datetime

class PurchaseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Categoria Teste')
        cls.item = Item.objects.create(name='Produto Teste', price=100, category=category)
        cls.vendor = Vendor.objects.create(name='Fornecedor Teste')

    def test_bootstrap_mixin_adds_form_control_class(self):
        form = PurchaseForm()
        for field in form.fields.values():
            self.assertIn('form-control', field.widget.attrs.get('class', ''))
    
    def test_form_is_valid_with_correct_data(self):
        form_data = {
            'item': self.item.pk,
            'price': 200.50,
            'description': 'Compra de teste',
            'vendor': self.vendor.pk,
            'quantity': 10,
            'delivery_date': datetime.datetime.now(),
            'delivery_status': 'P'
        }
        form = PurchaseForm(data=form_data)
        
        if not form.is_valid():
            print(form.errors.as_json())

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_if_required_fields_are_missing(self):
        form = PurchaseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('item', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('quantity', form.errors)