# invoice/tests/test_tables.py

from django.test import TestCase
from ..models import Invoice, Item
from ..tables import InvoiceTable
from store.models import Category # Importação necessária para criar o Item

class InvoiceTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Cria um Item e uma Invoice para serem usados nos testes.
        """
        category = Category.objects.create(name='Categoria Teste')
        item = Item.objects.create(name='Produto Teste', price=10.0, category=category)
        Invoice.objects.create(
            customer_name="Cliente Teste",
            contact_number="11999998888",
            item=item,
            price_per_item=25.50,
            quantity=2,
            shipping=10.0
        )

    def test_table_instantiation_and_row_count(self):
        """
        Verifica se a tabela é instanciada e se o número de linhas está correto.
        """
        queryset = Invoice.objects.all()
        table = InvoiceTable(queryset)
        self.assertEqual(len(table.rows), 1)

    def test_table_has_correct_columns(self):
        """
        Verifica se as colunas da tabela correspondem ao definido no Meta.fields.
        """
        table = InvoiceTable(Invoice.objects.none())
        
        expected_columns = [
            'date', 
            'customer_name', 
            'contact_number', 
            'item',
            'price_per_item', 
            'quantity', 
            'total'
        ]

        rendered_column_names = [col.name for col in table.columns]
        self.assertEqual(rendered_column_names, expected_columns)

    def test_table_meta_options_are_correct(self):
        """
        Verifica se as opções Meta da tabela estão configuradas corretamente.
        """
        self.assertEqual(InvoiceTable.Meta.model, Invoice)
        self.assertEqual(InvoiceTable.Meta.template_name, "django_tables2/semantic.html")
        self.assertEqual(InvoiceTable.Meta.order_by, "date")