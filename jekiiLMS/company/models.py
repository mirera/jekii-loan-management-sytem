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
    phone_no = models.CharField(max_length=10, default='0712345678')
    logo = models.ImageField(default='default.png', upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=30, default='active')
    is_license_expired = models.BooleanField(default=False) 
    address = models.CharField(max_length=100, default= 'SomeStreet')
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=10, default='USD')

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
    api_token = models.CharField(max_length=200, blank=True, null=True)#encrypted 

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