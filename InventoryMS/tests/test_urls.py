from django.test import SimpleTestCase
from django.urls import resolve
from django.contrib.auth import views as auth_views
from store import views as store_views
from accounts import views as accounts_views
from transactions import views as transactions_views
from invoice import views as invoice_views
from bills import views as bills_views

class RootUrlsTest(SimpleTestCase):
    

    def test_admin_url_resolves(self):
    
        resolver = resolve('/admin/')
        
        self.assertEqual(resolver.view_name, 'admin:index')

    def test_store_url_resolves_to_dashboard(self):
        
        resolver = resolve('/')
        self.assertEqual(resolver.func, store_views.dashboard)

    def test_staff_url_resolves_to_register(self):
        
        resolver = resolve('/staff/register/')
        self.assertEqual(resolver.func, accounts_views.register)
        
    def test_transactions_url_resolves_to_list(self):
       
        resolver = resolve('/transactions/purchases/')
        self.assertEqual(resolver.func.view_class, transactions_views.PurchaseListView)
        
    def test_accounts_url_resolves_to_login(self):
       
        resolver = resolve('/accounts/login/')
        self.assertEqual(resolver.func.view_class, auth_views.LoginView)

    def test_invoice_url_resolves_to_list(self):
        
        resolver = resolve('/invoice/invoices/')
        self.assertEqual(resolver.func.view_class, invoice_views.InvoiceListView)

    def test_bills_url_resolves_to_list(self):

        resolver = resolve('/bills/bills/')
        self.assertEqual(resolver.func.view_class, bills_views.BillListView)