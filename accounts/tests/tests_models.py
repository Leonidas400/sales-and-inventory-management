from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Vendor, Customer

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testuser123456789097654321',
            email='test@user.com'
        )
        self.profile = self.user.profile

    def test_profile_creation_and_defaults(self):
        self.assertIsNotNone(self.profile.pk)
        self.assertEqual(self.profile.status, 'INA')

    def test_autoslug_population_from_email(self):
        self.assertEqual(self.profile.slug, 'test-user-com')

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), "testuser Profile")

    def test_image_url_property(self):
        self.assertIn('profile_pics/default.jpg', self.profile.image_url)
        
        self.profile.profile_picture = None
        self.assertEqual(self.profile.image_url, '')


class VendorModelTest(TestCase):

    def test_vendor_creation_and_slug(self):
        vendor = Vendor.objects.create(name="Fornecedor Principal")
        self.assertEqual(str(vendor), "Fornecedor Principal")
        self.assertEqual(vendor.slug, "fornecedor-principal")

    def test_vendor_with_all_fields(self):
        vendor = Vendor.objects.create(
            name="Fornecedor Completo",
            phone_number=11987654321,
            address="Rua da Goiaba, 13"
        )
        self.assertEqual(vendor.phone_number, 11987654321)
        self.assertEqual(vendor.address, "Rua da Goiaba, 13")


class CustomerModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jorge",
            last_name="pereira"
        )

    def test_customer_default_loyalty_points(self):
        self.assertEqual(self.customer.loyalty_points, 0)

    def test_customer_str_method_and_get_full_name(self):
        expected_full_name = "Jorge pereira"
        self.assertEqual(str(self.customer), expected_full_name)
        self.assertEqual(self.customer.get_full_name(), expected_full_name)
        
    def test_to_select2_method(self):
        expected_dict = {
            "label": "Jorge pereira",
            "value": self.customer.id
        }
        self.assertEqual(self.customer.to_select2(), expected_dict)