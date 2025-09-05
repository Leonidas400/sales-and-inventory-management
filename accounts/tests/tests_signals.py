# accounts/tests/test_signals.py

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile

class SignalsTest(TestCase):

    def test_profile_is_created_when_user_is_created(self):
        """
        Verifica se um Profile é criado automaticamente quando um novo User é salvo.
        """
        # Garante que não existe nenhum Profile antes do teste
        self.assertEqual(Profile.objects.count(), 0)

        # Cria um novo usuário, o que deve disparar o signal
        user = User.objects.create_user(
            username='newuser', 
            password='password123', 
            email='new@user.com'
        )

        # Verifica se agora existe um Profile no banco de dados
        self.assertEqual(Profile.objects.count(), 1)
        # Verifica se o Profile criado está associado ao usuário correto
        self.assertEqual(Profile.objects.first().user, user)
        # Verifica se o email foi copiado corretamente
        self.assertEqual(Profile.objects.first().email, 'new@user.com')

    def test_profile_is_updated_when_user_is_updated(self):
        """
        Verifica se o Profile é atualizado quando o User correspondente é atualizado.
        """
        user = User.objects.create_user(
            username='updateuser', 
            password='password123', 
            email='original@email.com'
        )
        
        # Garante que o email inicial está correto
        self.assertEqual(user.profile.email, 'original@email.com')

        # Atualiza o email do usuário e salva, o que deve disparar o signal
        user.email = 'updated@email.com'
        user.save()

        # Pega o perfil novamente do banco de dados para garantir que estamos
        # vendo o dado mais recente
        user.profile.refresh_from_db()

        # Verifica se o email no perfil também foi atualizado
        self.assertEqual(user.profile.email, 'updated@email.com')

    def test_profile_is_created_for_existing_user_without_profile(self):
        """
        Verifica se o Profile é criado para um usuário existente que não o possui.
        """
        user = User.objects.create_user(
            username='existinguser', 
            password='password123', 
            email='existing@user.com'
        )
        # Deleta o perfil que foi criado pelo signal para simular a condição de erro
        user.profile.delete()
        
        # Verifica diretamente no banco de dados para evitar problemas de cache
        self.assertFalse(Profile.objects.filter(user=user).exists())

        # Salva o usuário novamente, o que deve acionar a lógica 'except Profile.DoesNotExist'
        user.save()

        # Verifica se o perfil foi recriado
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.email, 'existing@user.com')