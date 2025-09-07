import os
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile

class SignalsTest(TestCase):

    def test_profile_is_created_when_user_is_created(self):
        self.assertEqual(Profile.objects.count(), 0)

        username = os.environ.get('TEST_NEW_USER_USERNAME', 'newuser')
        password = os.environ.get('TEST_USER_PASSWORD', 'a-secure-password-123')
        email = os.environ.get('TEST_NEW_USER_EMAIL', 'new@example.com')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, user)
        self.assertEqual(Profile.objects.first().email, email)

    def test_profile_is_updated_when_user_is_updated(self):
        
        username = os.environ.get('TEST_UPDATE_USER_USERNAME', 'updateuser')
        password = os.environ.get('TEST_USER_PASSWORD', 'a-secure-password-123')
        original_email = os.environ.get('TEST_UPDATE_USER_EMAIL1', 'original@example.com')
        updated_email = os.environ.get('TEST_UPDATE_USER_EMAIL2', 'updated@example.com')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=original_email
        )
        
        self.assertEqual(user.profile.email, original_email)

        user.email = updated_email
        user.save()

        user.profile.refresh_from_db()

        self.assertEqual(user.profile.email, updated_email)

    def test_profile_is_created_for_existing_user_without_profile(self):
    
        username = os.environ.get('TEST_EXISTING_USER_USERNAME', 'existinguser')
        password = os.environ.get('TEST_USER_PASSWORD', 'a-secure-password-123')
        email = os.environ.get('TEST_EXISTING_USER_EMAIL', 'existing@example.com')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        user.profile.delete()
        
        self.assertFalse(Profile.objects.filter(user=user).exists())

        user.save()

        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.email, email)