from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile

class SignalsTest(TestCase):

    def test_profile_is_created_when_user_is_created(self):
        self.assertEqual(Profile.objects.count(), 0)

        user = User.objects.create_user(
            username='testenovo', 
            password='testi123456789', 
            email='test@novo.com'
        )

        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, user)
        self.assertEqual(Profile.objects.first().email, 'test@novo.com')

    def test_profile_is_updated_when_user_is_updated(self):
        user = User.objects.create_user(
            username='testeatualizado', 
            password='teste123456789', 
            email='oliginal@email.com'
        )
        
        self.assertEqual(user.profile.email, 'oliginal@email.com')

        user.email = 'testatualizado@email.com'
        user.save()

        user.profile.refresh_from_db()

        self.assertEqual(user.profile.email, 'testatualizado@email.com')

    def test_profile_is_created_for_existing_user_without_profile(self):
        user = User.objects.create_user(
            username='testexistente', 
            password='testo123456789', 
            email='estatualizado@email.com'
        )
        user.profile.delete()
        
        self.assertFalse(Profile.objects.filter(user=user).exists())

        user.save()

        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.email, 'estatualizado@email.com')