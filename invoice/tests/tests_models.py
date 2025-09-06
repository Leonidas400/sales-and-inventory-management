from django.test import TestCase
from ..models import Invoice
from store.models import Item, Category

class InvoiceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Categoria Teste')
        
        cls.item = Item.objects.create(
            name='Produto Makita', 
            price=10.0,
            category=category
        )

    def test_total_and_grand_total_are_calculated_on_save(self):
        invoice = Invoice(
            customer_name="Cliente Jorge",
            contact_number="11692793068",
            item=self.item,
            price_per_item=10.0,
            quantity=5,
            shipping=15.50
        )

        invoice.save()

        self.assertEqual(invoice.total, 50.00)
        self.assertEqual(invoice.grand_total, 65.50)

    def test_str_method_returns_slug(self):
        invoice = Invoice.objects.create(
            customer_name="Cliente Junin",
            contact_number="11968387965",
            item=self.item,
            price_per_item=20.0,
            quantity=2,
            shipping=10.0
        )
        self.assertIsNotNone(invoice.slug)
        self.assertEqual(str(invoice), invoice.slug)