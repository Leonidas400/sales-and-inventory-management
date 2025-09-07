import os
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Vendor, Customer

class ProfileModelTest(TestCase):

    def setUp(self):
        
        test_username = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'a-secure-password-123')
        test_email = os.environ.get('TEST_USER_EMAIL', 'test@example.com')

        self.user = User.objects.create_user(
            username=test_username,
            password=test_password,
            email=test_email
        )
        self.profile = self.user.profile

    def test_profile_creation_and_defaults(self):
        self.assertIsNotNone(self.profile.pk)
        self.assertEqual(self.profile.status, 'INA')

    def test_autoslug_population_from_email(self):
        
        expected_slug = os.environ.get('TEST_USER_EMAIL', 'test@example.com').replace('@', '-').replace('.', '-')
        self.assertEqual(self.profile.slug, expected_slug)

    def test_profile_str_method(self):
        test_username = os.environ.get('TEST_USER_USERNAME', 'testuser')
        self.assertEqual(str(self.profile), f"{test_username} Profile")

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
        
        test_phone = os.environ.get('TEST_VENDOR_PHONE', 11999999999)
        test_address = os.environ.get('TEST_VENDOR_ADDRESS', 'Rua dos Testes, 123')

        vendor = Vendor.objects.create(
            name="Fornecedor Completo",
            phone_number=test_phone,
            address=test_address
        )
        self.assertEqual(vendor.phone_number, int(test_phone))
        self.assertEqual(vendor.address, test_address)


class CustomerModelTest(TestCase):

    def setUp(self):
        
        test_first_name = os.environ.get('TEST_CUSTOMER_FNAME', 'João')
        test_last_name = os.environ.get('TEST_CUSTOMER_LNAME', 'Silva')

        self.customer = Customer.objects.create(
            first_name=test_first_name,
            last_name=test_last_name
        )

    def test_customer_default_loyalty_points(self):
        self.assertEqual(self.customer.loyalty_points, 0)

    def test_customer_str_method_and_get_full_name(self):
        test_first_name = os.environ.get('TEST_CUSTOMER_FNAME', 'João')
        test_last_name = os.environ.get('TEST_CUSTOMER_LNAME', 'Silva')
        expected_full_name = f"{test_first_name} {test_last_name}"

        self.assertEqual(str(self.customer), expected_full_name)
        self.assertEqual(self.customer.get_full_name(), expected_full_name)
        
    def test_to_select2_method(self):
        test_first_name = os.environ.get('TEST_CUSTOMER_FNAME', 'João')
        test_last_name = os.environ.get('TEST_CUSTOMER_LNAME', 'Silva')
        expected_label = f"{test_first_name} {test_last_name}"

        expected_dict = {
            "label": expected_label,
            "value": self.customer.id
        }
        self.assertEqual(self.customer.to_select2(), expected_dict)