from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User 




class Package(models.Model):
    name= models.CharField(max_length=100)
    annual_price = models.CharField(max_length=100)
    monthly_price = models.CharField(max_length=100)
    employees = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    #date_added = models.DateField(auto_now_add=True)
    #modules = models.ManyToManyField(Models)

    def __str__(self):
        return self.name
    


STATUS = (
    ('active','ACTIVE'),
    ('inactive', 'INACTIVE')
)
#organization model
class Organization(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=12, default='712345678')
    logo = models.ImageField(default='default.png', upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=30, default='active')
    is_license_expired = models.BooleanField(default=False) 
    address = models.CharField(max_length=100, default= 'SomeStreet')
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=10, default='USD')
    country = models.CharField(max_length=30, default='Kenya')
    phone_code = models.CharField(max_length=5, default='1') 
    paybill_no = models.CharField(max_length=12, blank=True, null=True)
    account_no = models.CharField(max_length=15, blank=True, null=True)
 

    def get_localized_datetime(self, datetime_value):
        user_timezone = timezone.pytz.timezone(self.timezone)
        localized_datetime = datetime_value.astimezone(user_timezone)
        return localized_datetime

    def __str__(self):
        return self.name

#sms setting model
class SmsSetting(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True, )
    sender_id = models.CharField(max_length=15, blank=True, null=True)
    api_token = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company.name
# -- ends 

#mpesa setting model
class MpesaSetting(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    shortcode = models.IntegerField(blank=True, null=True)
    app_consumer_key = models.CharField(max_length=200, blank=True, null=True)#encrypted 
    app_consumer_secret = models.CharField(max_length=200, blank=True, null=True)#encrypted 
    online_passkey = models.CharField(max_length=200, blank=True, null=True)#encrypted
    username = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.company.name 
# -- ends 

#email setting model
HTTPS_ENCRYPTION = (
    ('tls','TLS'),
    ('ssl', 'SSL'),
    ('none', 'NONE')
)
class EmailSetting(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    from_name = models.CharField(max_length=15, blank=True, null=True)
    from_email = models.EmailField(blank=True, null=True)
    smtp_host = models.CharField(max_length=200, blank=True, null=True)
    encryption = models.CharField(max_length=10, choices=HTTPS_ENCRYPTION, default='tls')
    smtp_port = models.IntegerField(blank=True, null=True)
    smtp_username = models.EmailField(blank=True, null=True)
    smtp_password = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company.name
# -- ends 

#system setting model
class SystemSetting(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True, )
    is_auto_disburse = models.BooleanField(default=False)
    is_send_sms = models.BooleanField(default=False)
    is_send_email = models.BooleanField(default=False)
    #sms member
    on_joining = models.BooleanField(default=False)
    loan_pending = models.BooleanField(default=False)
    before_due_date = models.BooleanField(default=False)
    missed_payment = models.BooleanField(default=False)
    loan_rejected = models.BooleanField(default=False)
    #email member
    monthly_loan_statement = models.BooleanField(default=False)
    new_loan_products = models.BooleanField(default=False)
    #email staff
    monthly_portfolio_performance = models.BooleanField(default=False)
   

    def __str__(self):
        return self.company.name
# -- ends 

#security setting model
class SecuritySetting(models.Model):
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True, )
    #save_activity = models.BooleanField(default=True)
    two_fa_auth = models.BooleanField(default=True)
    #auto_logout = models.BooleanField(default=True)

    def __str__(self):
        return self.company.name
# -- ends


#template setting model
class TemplateSetting(models.Model): 
    company = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    member_welcome = models.TextField(default="Dear {first_name} {last_name}, welcome to {organization_name}. Access business loans & scale your business.")
    loan_applied = models.TextField(default="Dear {first_name} {last_name}, Your loan request as been received and its under review. Regards {organization_name}")
    loan_rejected = models.TextField(default="Dear {first_name}, we regret to inform you that we are unable to approve your loan request of {currency}{applied_amount} at this time. ")
    loan_approved = models.TextField(default="Dear {first_name}, Your loan request has been approved and queued for disbursal. The next payment date {due_date}, amount {currency}{due_amount}. Acc. {account_no} Paybill {paybill_no}")
    loan_cleared = models.TextField(default="Dear {first_name} {last_name}, You have successfully cleared your loan. Success in your business. {organization_name}")
    loan_overdue = models.TextField(default="Dear {first_name}, your loan installment of {currency}{due_amount} is overdue. Make payment to avoid further penalties. Acc. no: {account_no} Paybill:{paybill_no}")
    loan_balance = models.TextField(default="Dear {first_name}, your next payment is on {due_date}. Due amount: {currency}{due_amount} . Loan balance: {currency}{loan_balance}. Acc. No: {account_no} Paybill:{paybill_no}")
    after_payment = models.TextField(default="Dear {first_name}, your next payment is on {due_date}. Due amount: {currency}{due_amount} . Loan balance: {currency}{loan_balance}. Acc. no: {account_no} Paybill:{paybill_no}")

    def __str__(self):
        return self.company.name
# -- ends 