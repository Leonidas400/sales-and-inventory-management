# accounts/tests/test_tables.py

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile
from ..tables import ProfileTable

class ProfileTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Cria um usuário e um perfil com os campos esperados pela tabela.
        """
        user = User.objects.create_user(username='testuser', 
        password='password123',
        email='test@user.com')
        profile = user.profile
        profile.first_name = "Cliente"
        profile.last_name = "Teste"
        profile.telephone = "+5511999998888"
        profile.save()

    def test_table_instantiation_and_row_count(self):
        """
        Verifica se a tabela é instanciada e se o número de linhas está correto.
        """
        queryset = Profile.objects.all()
        table = ProfileTable(queryset)
        self.assertEqual(len(table.rows), 1)

    def test_table_has_correct_columns(self):
        """
        Verifica se as colunas da tabela correspondem ao definido no Meta.fields.
        """
        # Usamos um queryset vazio, pois só queremos checar a estrutura da tabela
        table = ProfileTable(Profile.objects.none())
        
        expected_columns = [
            'date',
            'customer_name',
            'contact_number',
            'item',
            'price_per_item',
            'quantity',
            'total'
        ]

        rendered_column_names = [col.name for col in table.columns]
        self.assertEqual(rendered_column_names, expected_columns)

    def test_table_meta_options_are_correct(self):
        """
        Verifica se as opções Meta da tabela estão configuradas corretamente.
        """
        self.assertEqual(ProfileTable.Meta.model, Profile)
        self.assertEqual(ProfileTable.Meta.template_name, "django_tables2/semantic.html")
        self.assertEqual(ProfileTable.Meta.order_by_field, "sort")