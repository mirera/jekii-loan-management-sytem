from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CompanyStaff

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=CompanyStaff)
def set_default_profilephoto(sender, instance, **kwargs):
    if not instance.profile_photo:
        instance.profile_photo = 'default.png'