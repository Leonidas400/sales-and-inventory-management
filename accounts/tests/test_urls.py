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
        url = reverse('user-login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_profile_list_url_resolves(self):
        url = reverse('profile_list')
        self.assertEqual(resolve(url).func.view_class, ProfileListView)

    def test_profile_update_url_resolves(self):
        url = reverse('profile-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)
    
    def test_customer_list_url_resolves(self):
        url = reverse('customer_list')
        self.assertEqual(resolve(url).func.view_class, CustomerListView)
    
    def test_customer_delete_url_resolves(self):
        url = reverse('customer_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, CustomerDeleteView)

    def test_vendor_list_url_resolves(self):
        url = reverse('vendor-list')
        self.assertEqual(resolve(url).func.view_class, VendorListView)
        
    def test_vendor_create_url_resolves(self):
        url = reverse('vendor-create')
        self.assertEqual(resolve(url).func.view_class, VendorCreateView)