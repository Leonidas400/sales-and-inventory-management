# transactions/tests/test_forms.py

from django.test import TestCase
from ..forms import PurchaseForm
from store.models import Item, Category
from accounts.models import Vendor
import datetime

class PurchaseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Cria objetos relacionados para serem usados nos testes do formulário."""
        category = Category.objects.create(name='Categoria Teste')
        cls.item = Item.objects.create(name='Produto Teste', price=100, category=category)
        cls.vendor = Vendor.objects.create(name='Fornecedor Teste')

    def test_bootstrap_mixin_adds_form_control_class(self):
        """Verifica se o BootstrapMixin adiciona a classe 'form-control' aos campos."""
        form = PurchaseForm()
        for field in form.fields.values():
            self.assertIn('form-control', field.widget.attrs.get('class', ''))
    
    def test_form_is_valid_with_correct_data(self):
        """Verifica se o formulário é válido ao receber dados corretos."""
        form_data = {
            'item': self.item.pk,
            'price': 200.50,
            'description': 'Compra de teste',
            'vendor': self.vendor.pk,
            'quantity': 10,
            'delivery_date': datetime.datetime.now(),
            # --- CORREÇÃO APLICADA AQUI ---
            'delivery_status': 'P' # Usando o valor real ('P') em vez do rótulo ('Pending')
        }
        form = PurchaseForm(data=form_data)
        
        # Adiciona um print para depuração caso o formulário ainda seja inválido
        if not form.is_valid():
            print(form.errors.as_json())

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_if_required_fields_are_missing(self):
        """Verifica se o formulário é inválido quando dados obrigatórios faltam."""
        form = PurchaseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('item', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('quantity', form.errors)