from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Organization

#setting the logo default to 'default.png'
@receiver(pre_save, sender=Organization)
def set_default_logo(sender, instance, **kwargs):
    if not instance.logo:
        instance.logo = 'default-logo.png'