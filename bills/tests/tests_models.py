from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from ..models import Bill

class BillModelTest(TestCase):

    def test_bill_creation_with_required_fields(self):
        bill = Bill.objects.create(
            institution_name="Hospital Santo Amaro",
            payment_details="Consulta de rotina",
            amount=250.50
        )
        self.assertIsNotNone(bill.pk)
        self.assertEqual(bill.institution_name, "Hospital Santo Amaro")
        self.assertEqual(bill.amount, 250.50)
        self.assertFalse(bill.status)

    def test_str_method_returns_institution_name(self):
        bill = Bill.objects.create(
            institution_name="Clínica Sorriso",
            payment_details="Tratamento",
            amount=150.00
        )
        self.assertEqual(str(bill), "Clínica Sorriso")

    def test_autoslug_field_is_populated(self):
        bill = Bill.objects.create(
            institution_name="Laboratório Teste Rapido",
            payment_details="Exames",
            amount=80.00
        )
        self.assertIsNotNone(bill.slug)
        self.assertNotEqual(bill.slug, "")

    def test_bill_with_all_fields(self):
        bill = Bill.objects.create(
            institution_name="Escola Educar",
            phone_number=11783656329,
            email="contato@escolaeducar.com",
            address="Rua Acre, 27",
            description="Mensalidade de Outubro",
            payment_details="Boleto Bancário",
            amount=550.00,
            status=True
        )
        self.assertEqual(bill.phone_number, 11783656329)
        self.assertEqual(bill.email, "contato@escolaeducar.com")
        self.assertTrue(bill.status)

    def test_required_fields_raise_validation_error(self):
        bill_no_name = Bill(payment_details="Payment", amount=100.00)
        with self.assertRaises(ValidationError):
            bill_no_name.full_clean()

        bill_no_details = Bill(institution_name="Store XYZ", amount=100.00)
        with self.assertRaises(ValidationError):
            bill_no_details.full_clean()