# invoice/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Invoice
from store.models import Item, Category

class InvoiceViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Cria dados iniciais para todos os testes: um usuário normal, um superusuário,
        um Item (com Categoria) e uma Invoice.
        """
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        
        category = Category.objects.create(name='Categoria Teste')
        cls.item = Item.objects.create(name='Produto Teste', price=10.0, category=category)
        
        cls.invoice = Invoice.objects.create(
            customer_name="Cliente Teste",
            contact_number="11999998888",
            item=cls.item,
            price_per_item=50.0,
            quantity=2,
            shipping=15.0
        )

    def test_list_view_requires_login(self):
        """Verifica se a lista de faturas redireciona se o usuário não estiver logado."""
        response = self.client.get(reverse('invoicelist'))
        self.assertRedirects(response, f"{reverse('user-login')}?next={reverse('invoicelist')}")

    def test_list_view_is_accessible_by_logged_in_user(self):
        """Verifica se um usuário logado pode acessar a lista de faturas."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('invoicelist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoice/invoicelist.html')
        self.assertContains(response, self.invoice.customer_name)

    def test_detail_view_is_accessible(self):
        """Verifica se a página de detalhes da fatura carrega."""
        # A DetailView não tem LoginRequiredMixin, então deve ser pública
        response = self.client.get(reverse('invoice-detail', args=[self.invoice.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoice/invoicedetail.html')

    def test_create_view_post_creates_invoice(self):
        """Verifica se um usuário logado pode criar uma nova fatura via POST."""
        self.client.login(username='testuser', password='password123')
        initial_invoice_count = Invoice.objects.count()
        response = self.client.post(reverse('invoice-create'), {
            'customer_name': 'Novo Cliente',
            'contact_number': '11987654321',
            'item': self.item.pk,
            'price_per_item': 20.0,
            'quantity': 3,
            'shipping': 5.0
        })
        self.assertEqual(Invoice.objects.count(), initial_invoice_count + 1)
        self.assertRedirects(response, reverse('invoicelist'))

    def test_update_view_permission_denied_for_normal_user(self):
        """Verifica se um usuário normal não pode atualizar uma fatura."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('invoice-update', args=[self.invoice.slug]))
        self.assertEqual(response.status_code, 403) # 403 Forbidden

    def test_update_view_post_by_superuser(self):
        """Verifica se um superusuário pode atualizar uma fatura."""
        self.client.login(username='superuser', password='password123')
        response = self.client.post(reverse('invoice-update', args=[self.invoice.slug]), {
            'customer_name': 'Cliente Atualizado',
            'contact_number': self.invoice.contact_number,
            'item': self.invoice.item.pk,
            'price_per_item': self.invoice.price_per_item,
            'quantity': self.invoice.quantity,
            'shipping': self.invoice.shipping,
        })
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.customer_name, 'Cliente Atualizado')
        self.assertRedirects(response, reverse('invoicelist'))

    def test_delete_view_post_by_superuser(self):
        """Verifica se um superusuário pode deletar uma fatura."""
        self.client.login(username='superuser', password='password123')
        initial_invoice_count = Invoice.objects.count()
        response = self.client.post(reverse('invoice-delete', args=[self.invoice.pk]))
        self.assertEqual(Invoice.objects.count(), initial_invoice_count - 1)
        self.assertRedirects(response, reverse('invoicelist'))