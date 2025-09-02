# bills/tests/test_tables.py

from django.test import TestCase
from ..models import Bill
from ..tables import BillTable

class BillTableTest(TestCase):
    """Test suite for the BillTable."""

    @classmethod
    def setUpTestData(cls):
        """
        Cria dados de teste uma vez para toda a classe.
        Este método é o mais eficiente para criar objetos que não serão
        modificados durante os testes.
        """
        Bill.objects.create(
            institution_name="Hospital Central",
            payment_details="Consulta",
            amount=150.00
        )
        Bill.objects.create(
            institution_name="Clínica Sorriso",
            payment_details="Tratamento",
            amount=300.50
        )

    def test_table_instantiation_and_row_count(self):
        """
        Verifica se a tabela é instanciada corretamente e se o número de linhas
        corresponde ao número de objetos no banco de dados.
        """
        queryset = Bill.objects.all()
        table = BillTable(queryset)
        self.assertEqual(len(table.rows), 2)

    def test_table_has_correct_columns_in_order(self):
        """
        Verifica se as colunas da tabela correspondem EXATAMENTE
        ao que foi definido no Meta.fields, INCLUINDO A ORDEM.
        """
        table = BillTable(Bill.objects.none())
        
        expected_columns = [
            'date',
            'institution_name',
            'phone_number',
            'email',
            'address',
            'description',
            'payment_details',
            'amount',
            'status'
        ]

        rendered_columns = [col.name for col in table.columns]
        self.assertEqual(rendered_columns, expected_columns)

    def test_table_contains_all_expected_columns_order_independent(self):
        """
        (TESTE ADICIONAL E MAIS ROBUSTO)
        Verifica se a tabela contém todas as colunas esperadas,
        INDEPENDENTEMENTE DA ORDEM em que foram declaradas.
        """
        table = BillTable(Bill.objects.none())
        
        expected_columns = {
            'date',
            'institution_name',
            'phone_number',
            'email',
            'address',
            'description',
            'payment_details',
            'amount',
            'status'
        }

        rendered_columns = {col.name for col in table.columns}
        # assertCountEqual verifica se os dois conjuntos têm os mesmos itens,
        # sem se importar com a ordem.
        self.assertCountEqual(rendered_columns, expected_columns)

    def test_table_meta_options_are_correct(self):
        """
        Verifica se as opções Meta (template, etc.) estão configuradas corretamente.
        """
        self.assertEqual(BillTable.Meta.model, Bill)
        self.assertEqual(BillTable.Meta.template_name, "django_tables2/semantic.html")
        self.assertEqual(BillTable.Meta.order_by_field, "sort")