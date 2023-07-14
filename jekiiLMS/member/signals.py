from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member
from company.models import SmsSetting, SystemSetting, TemplateSetting
from jekiiLMS.sms_messages import send_sms
from jekiiLMS.tasks import  send_sms_task

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
        template_setting = TemplateSetting.objects.get(company=instance.company)
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token

        #available tags 
        first_name = instance.first_name
        last_name = instance.last_name
        organization_name = instance.company.name

        #format raw message template 
        message_raw = template_setting.member_welcome # is a string "Dear {first_name}"
        message = message_raw.format(first_name=first_name, last_name=last_name, organization_name=organization_name)
        preferences = SystemSetting.objects.get(company=instance.company)
        
        if preferences.is_send_sms and preferences.on_joining and sender_id is not None and token is not None:
            send_sms_task.delay(
                sender_id,
                token,
                instance.phone_no,
                message
            )
# -- ends