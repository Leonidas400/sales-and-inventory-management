# accounts/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Vendor, Customer

class ProfileModelTest(TestCase):

    def setUp(self):
        """Cria um usuário base para os testes do Profile."""
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123',
            email='test@user.com'
        )
        # Assumimos que um signal cria o Profile automaticamente
        self.profile = self.user.profile

    def test_profile_creation_and_defaults(self):
        """Verifica se o Profile é criado e se os valores padrão estão corretos."""
        self.assertIsNotNone(self.profile.pk)
        self.assertEqual(self.profile.status, 'INA')

    def test_autoslug_population_from_email(self):
        """Verifica se o slug foi populado a partir do email do usuário."""
        self.assertEqual(self.profile.slug, 'test-user-com')

    def test_profile_str_method(self):
        """Verifica o método __str__ do Profile."""
        self.assertEqual(str(self.profile), "testuser Profile")

    def test_image_url_property(self):
        """Verifica a propriedade 'image_url'."""
        # Um perfil recém-criado usa a imagem padrão
        self.assertIn('profile_pics/default.jpg', self.profile.image_url)
        
        # Simula a remoção da imagem para testar o 'except'
        self.profile.profile_picture = None
        self.assertEqual(self.profile.image_url, '')


class VendorModelTest(TestCase):

    def test_vendor_creation_and_slug(self):
        """Verifica a criação de um Vendor e seu slug."""
        vendor = Vendor.objects.create(name="Fornecedor Principal")
        self.assertEqual(str(vendor), "Fornecedor Principal")
        self.assertEqual(vendor.slug, "fornecedor-principal")

    def test_vendor_with_all_fields(self):
        """Verifica a criação de um Vendor com todos os campos."""
        vendor = Vendor.objects.create(
            name="Fornecedor Completo",
            phone_number=11987654321,
            address="Rua dos Testes, 123"
        )
        self.assertEqual(vendor.phone_number, 11987654321)
        self.assertEqual(vendor.address, "Rua dos Testes, 123")


class CustomerModelTest(TestCase):

    def setUp(self):
        """Cria um cliente base para os testes do Customer."""
        self.customer = Customer.objects.create(
            first_name="João",
            last_name="Silva"
        )

    def test_customer_default_loyalty_points(self):
        """Verifica se os pontos de lealdade iniciam em zero."""
        self.assertEqual(self.customer.loyalty_points, 0)

    def test_customer_str_method_and_get_full_name(self):
        """Verifica os métodos __str__ e get_full_name do Customer."""
        expected_full_name = "João Silva"
        self.assertEqual(str(self.customer), expected_full_name)
        self.assertEqual(self.customer.get_full_name(), expected_full_name)
        
    def test_to_select2_method(self):
        """Verifica se o método to_select2 retorna o dicionário correto."""
        expected_dict = {
            "label": "João Silva",
            "value": self.customer.id
        }
        self.assertEqual(self.customer.to_select2(), expected_dict)