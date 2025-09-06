from django.test import TestCase
from ..models import Bill
from ..tables import BillTable

class BillTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Bill.objects.create(
            institution_name="Hospital Santo Amaro",
            payment_details="Consulta",
            amount=150.00
        )
        Bill.objects.create(
            institution_name="Clínica Sorriso",
            payment_details="Tratamento",
            amount=300.50
        )

    def test_table_instantiation_and_row_count(self):
        queryset = Bill.objects.all()
        table = BillTable(queryset)
        self.assertEqual(len(table.rows), 2)

    def test_table_has_correct_columns_in_order(self):
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
        self.assertCountEqual(rendered_columns, expected_columns)

    def test_table_meta_options_are_correct(self):
        self.assertEqual(BillTable.Meta.model, Bill)
        self.assertEqual(BillTable.Meta.template_name, "django_tables2/semantic.html")
        self.assertEqual(BillTable.Meta.order_by_field, "sort")