from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from jekiiLMS.sms_messages import send_sms

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=Member)
def set_default_passport_photo(sender, instance, **kwargs):
    if not instance.passport_photo:
        instance.passport_photo = 'default.png'

@receiver(post_save, sender=Member)
def welcom_member_sms(sender, instance, created, **kwargs):
    if created:
        message = f"Dear {instance.first_name} {instance.last_name}, welcome to {instance.company.name}. Access business loans & scale your business"
        send_sms(instance.phone_no, message)
