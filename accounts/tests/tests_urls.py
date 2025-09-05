# accounts/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from accounts import views as user_views
from ..views import (
    ProfileListView,
    ProfileCreateView,
    ProfileUpdateView,
    ProfileDeleteView,
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    get_customers,
    VendorListView,
    VendorCreateView,
    VendorUpdateView,
    VendorDeleteView
)

class AccountsUrlsTest(SimpleTestCase):

    def test_login_url_resolves(self):
        """Verifica se a URL de login resolve para a view correta."""
        url = reverse('user-login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_profile_list_url_resolves(self):
        """Verifica se a URL da lista de perfis resolve para a view correta."""
        url = reverse('profile_list')
        self.assertEqual(resolve(url).func.view_class, ProfileListView)

    def test_profile_update_url_resolves(self):
        """Verifica se a URL de atualização de perfil resolve para a view correta."""
        # Para URLs com parâmetros, passamos um argumento de exemplo.
        url = reverse('profile-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)
    
    def test_customer_list_url_resolves(self):
        """Verifica se a URL da lista de clientes resolve para a view correta."""
        url = reverse('customer_list')
        self.assertEqual(resolve(url).func.view_class, CustomerListView)
    
    def test_customer_delete_url_resolves(self):
        """Verifica se a URL de exclusão de cliente resolve para a view correta."""
        url = reverse('customer_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, CustomerDeleteView)

    def test_vendor_list_url_resolves(self):
        """Verifica se a URL da lista de fornecedores resolve para a view correta."""
        url = reverse('vendor-list')
        self.assertEqual(resolve(url).func.view_class, VendorListView)
        
    def test_vendor_create_url_resolves(self):
        """Verifica se a URL de criação de fornecedor resolve para a view correta."""
        url = reverse('vendor-create')
        self.assertEqual(resolve(url).func.view_class, VendorCreateView)