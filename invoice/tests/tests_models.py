# invoice/tests/test_models.py

from django.test import TestCase
from ..models import Invoice
from store.models import Item, Category # Importação do Category é necessária

class InvoiceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Cria os objetos Categoria e Item necessários para os testes da Invoice.
        """
        # 1. Cria uma Categoria primeiro
        category = Category.objects.create(name='Categoria Teste')
        
        # 2. Associa o Item a essa Categoria ao criá-lo
        cls.item = Item.objects.create(
            name='Produto Teste', 
            price=10.0,
            category=category
        )

    def test_total_and_grand_total_are_calculated_on_save(self):
        invoice = Invoice(
            customer_name="Cliente A",
            contact_number="11999998888",
            item=self.item,
            price_per_item=10.0,
            quantity=5,
            shipping=15.50
        )

        # Salva o objeto, o que dispara o método save() customizado
        invoice.save()

        # Verifica se os cálculos foram feitos corretamente
        self.assertEqual(invoice.total, 50.00) # 5 * 10.0
        self.assertEqual(invoice.grand_total, 65.50) # 50.00 + 15.50

    def test_str_method_returns_slug(self):
        """Verifica se o método __str__ retorna o slug."""
        invoice = Invoice.objects.create(
            customer_name="Cliente B",
            contact_number="11988887777",
            item=self.item,
            price_per_item=20.0,
            quantity=2,
            shipping=10.0
        )
        # O __str__ deve retornar o slug, que é gerado automaticamente
        self.assertIsNotNone(invoice.slug)
        self.assertEqual(str(invoice), invoice.slug)