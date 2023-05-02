
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan
from member.models import Member

@receiver(post_save, sender=Loan)
def update_member_status(sender, instance, **kwargs):
    if instance.status in ['approved', 'overdue']:
        member = instance.member
        if not member.has_active_loan():
            member.status = 'inactive'
            member.save()

