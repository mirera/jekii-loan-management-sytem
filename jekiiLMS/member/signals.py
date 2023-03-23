from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Member

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=Member)
def set_default_passport_photo(sender, instance, **kwargs):
    if not instance.passport_photo:
        instance.passport_photo = 'default.png'
