from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    
    if created:
        Profile.objects.create(user=instance, email=instance.email)
        print('Profile created!')
    else:
        try:
            profile = instance.profile
            if profile.email != instance.email:
                profile.email = instance.email
                profile.save()
            print('Profile updated!')
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance, email=instance.email)
            print('Profile created for existing user!')