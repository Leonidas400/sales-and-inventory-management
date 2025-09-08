import os
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile

class SignalsTest(TestCase):

    def test_profile_is_created_when_user_is_created(self):
        self.assertEqual(Profile.objects.count(), 0)
        user = User.objects.create_user(
            username='newuser',
            password='a-secure-password-123',
            email='new@example.com'
        )
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, user)
        self.assertEqual(Profile.objects.first().email, 'new@example.com')

    def test_profile_email_is_updated_when_user_email_changes(self):
        user = User.objects.create_user(
            username='updateuser',
            password='a-secure-password-123',
            email='original@example.com'
        )
        self.assertEqual(user.profile.email, 'original@example.com')
        
        user.email = 'updated@example.com'
        user.save()
        
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.email, 'updated@example.com')

    def test_profile_save_is_not_called_if_email_is_unchanged(self):
        """
        (NOVO TESTE) Verifica se profile.save() NÃO é chamado se o e-mail não mudar.
        Isso cobre a lógica 'if profile.email != instance.email:'.
        """
        user = User.objects.create_user(
            username='samesame',
            password='a-secure-password-123',
            email='same@example.com'
        )
        
        # Usamos 'patch' para "espionar" o método .save() do Profile
        with patch('accounts.models.Profile.save') as mock_save:
            # Salvamos o usuário novamente, mas sem alterar o e-mail
            user.save()
            # Verificamos se o método .save() do Profile NÃO foi chamado
            mock_save.assert_not_called()

    def test_profile_is_created_for_existing_user_without_profile(self):
        user = User.objects.create_user(
            username='existinguser',
            password='a-secure-password-123',
            email='existing@example.com'
        )
        user.profile.delete()
        
        self.assertFalse(Profile.objects.filter(user=user).exists())
        user.save()
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.email, 'existing@example.com')