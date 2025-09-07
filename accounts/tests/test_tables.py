import os
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile
from ..tables import ProfileTable

class ProfileTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        test_username = os.environ.get('TEST_USER_USERNAME', 'testuser')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'a-secure-password-123')
        test_email = os.environ.get('TEST_USER_EMAIL', 'test@example.com')
        test_phone = os.environ.get('TEST_USER_PHONE', '+5511999998888')

        user = User.objects.create_user(
            username=test_username, 
            password=test_password,
            email=test_email
        )
        profile = user.profile
        profile.first_name = "Cliente"
        profile.last_name = "Teste"
        profile.telephone = test_phone
        profile.save()

    def test_table_instantiation_and_row_count(self):
        queryset = Profile.objects.all()
        table = ProfileTable(queryset)
        self.assertEqual(len(table.rows), 1)

    def test_table_has_correct_columns(self):
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
        self.assertEqual(ProfileTable.Meta.model, Profile)
        self.assertEqual(ProfileTable.Meta.template_name, "django_tables2/semantic.html")
        self.assertEqual(ProfileTable.Meta.order_by_field, "sort")