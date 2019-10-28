from django.db.models.signals import post_save
from .models import Account
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('wow')

@receiver(post_save, sender=Account)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
