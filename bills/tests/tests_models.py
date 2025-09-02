# bills/tests.py

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError # <--- 1. IMPORTAÇÃO ADICIONADA
from ..models import Bill

class BillModelTest(TestCase):
    """Test suite for the Bill model."""

    def test_bill_creation_with_required_fields(self):
        """
        Tests that a Bill instance can be created with required fields
        and that default values are set correctly.
        """
        bill = Bill.objects.create(
            institution_name="Hospital Central",
            payment_details="Consulta de rotina",
            amount=250.50
        )
        self.assertIsNotNone(bill.pk)
        self.assertEqual(bill.institution_name, "Hospital Central")
        self.assertEqual(bill.amount, 250.50)
        self.assertFalse(bill.status)

    def test_str_method_returns_institution_name(self):
        """
        Tests the __str__ method to ensure it returns the institution's name.
        """
        bill = Bill.objects.create(
            institution_name="Clínica Sorriso",
            payment_details="Tratamento",
            amount=150.00
        )
        self.assertEqual(str(bill), "Clínica Sorriso")

    def test_autoslug_field_is_populated(self):
        """
        Tests that the slug is automatically generated and saved.
        """
        bill = Bill.objects.create(
            institution_name="Laboratório Vida",
            payment_details="Exames",
            amount=80.00
        )
        self.assertIsNotNone(bill.slug)
        self.assertNotEqual(bill.slug, "")

    # 2. TESTE ANTIGO E INCORRETO FOI REMOVIDO DESTA VERSÃO

    def test_bill_with_all_fields(self):
        """
        Tests creating a Bill instance with all optional fields populated.
        """
        bill = Bill.objects.create(
            institution_name="Escola Aprender",
            phone_number=11987654321,
            email="contato@escola.com",
            address="Rua do Saber, 123",
            description="Mensalidade de Outubro",
            payment_details="Boleto Bancário",
            amount=550.00,
            status=True
        )
        # 3. VERIFICAÇÕES MOVIDAS PARA O LUGAR CERTO
        self.assertEqual(bill.phone_number, 11987654321)
        self.assertEqual(bill.email, "contato@escola.com")
        self.assertTrue(bill.status)

    def test_required_fields_raise_validation_error(self):
        """
        Tests that required fields raise a ValidationError when calling full_clean().
        """
        # Test without institution_name
        bill_no_name = Bill(payment_details="Payment", amount=100.00)
        with self.assertRaises(ValidationError):
            bill_no_name.full_clean()

        # Test without payment_details
        bill_no_details = Bill(institution_name="Store XYZ", amount=100.00)
        with self.assertRaises(ValidationError):
            bill_no_details.full_clean()