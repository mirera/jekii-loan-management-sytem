from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from company.models import SmsSetting, SystemSetting
from jekiiLMS.sms_messages import send_sms

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=Member)
def set_default_passport_photo(sender, instance, **kwargs):
    if not instance.passport_photo:
        instance.passport_photo = 'default.png'
# --ends

#func begins
@receiver(post_save, sender=Member)
def welcom_member_sms(sender, instance, created, **kwargs):
    if created:
        sms_setting = SmsSetting.objects.get(company=instance.company)
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token
        message = f"Dear {instance.first_name} {instance.last_name}, welcome to {instance.company.name}. Access business loans & scale your business"
        preferences = SystemSetting.objects.get(company=instance.company)
        if preferences.is_send_sms and sender_id is not None and token is not None:
            send_sms(
                sender_id,
                token,
                instance.phone_no,
                message
            )
# -- ends