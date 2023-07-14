from dataclasses import fields
from django import forms
from pytz import all_timezones
from iso4217 import Currency
import pycountry
from .models import Organization, Package, SmsSetting, MpesaSetting, EmailSetting, SystemSetting, SecuritySetting, TemplateSetting
from jekiiLMS.utils import phone_codes


class OrganizationForm(forms.ModelForm): 

    all_currencies = [currency.code for currency in Currency] 


    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in all_timezones],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    currency = forms.ChoiceField(
        choices=[(curr, curr) for curr in all_currencies],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.ChoiceField(
        choices=[(country.alpha_2, country.name) for country in pycountry.countries],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    phone_code = forms.ChoiceField(
        choices=phone_codes,
        widget=forms.Select(attrs={'class': 'form-control ', 'style':'background-color:#ebeef2;'})
    )



    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['admin', 'date_joined']
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control', 'minlength':'10'}),
            'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id':'customFile', 'type':'file'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'paybill_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'522522'}),
            'account_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'5840988'}),
        }

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':'True'}),
            'annual_price': forms.NumberInput(attrs={'class': 'form-control', 'required':'True'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control', 'required':'True'}),
            'employees': forms.NumberInput(attrs={'class': 'form-control', 'required':'True'}),
            'storage': forms.TextInput(attrs={'class': 'form-control', 'id': 'site-address', 'required':'True'}),
        }

class SmsForm(forms.ModelForm):
    class Meta:
        model = SmsSetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            'sender_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'loginit', 'required':'True'}),
            'api_token': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG', 'required':'True'}),
        }

class MpesaSettingForm(forms.ModelForm):
    class Meta:
        model = MpesaSetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            'shortcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '174379', 'required':'True'}),
            'app_consumer_key': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG', 'required':'True'}),
            'app_consumer_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG', 'required':'True'}),
            'online_passkey': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'e.g 9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG', 'required':'True'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'loginit', 'required':'True'}),
        }

class EmailSettingForm(forms.ModelForm):
    class Meta:
        model = EmailSetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            'from_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Loginit CyberSec', 'required':'True'}),
            'from_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. info@loginit.co.ke', 'required':'True'}),
            'smtp_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. smtp.loginit.com', 'required':'True'}),
            'encryption': forms.Select(attrs={'class': 'form-select js-select2'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 587', 'required':'True'}),
            'smtp_username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g info@loginit.com', 'required':'True'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'form-control', 'required':'True'}),
        }

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            'is_auto_disburse': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'auto_disburse'}),
            'is_send_sms': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'send_sms'}), 
            'is_send_email': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'send_email'}), 
            'on_joining': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'on_joining'}),
            'loan_pending': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'loan-pending'}), 
            'before_due_date': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'before-due-date'}), 

            'missed_payment': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'missed-payment'}),

            'loan_rejected': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'loan-rejected'}),

            'monthly_loan_statement': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'loan-statement'}),
            'new_loan_products': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'new-product'}), 
            'monthly_portfolio_performance': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'portfolio-performance'}),  
        }

class SecuritySettingForm(forms.ModelForm): 
    class Meta:
        model = SecuritySetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            #'save_activity': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'save_activity'}),
            'two_fa_auth': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'two_fa_auth'}), 
            #'auto_logout': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'auto_logout'}),    
        }

class TemplateForm(forms.ModelForm):
    class Meta:
        model = TemplateSetting
        fields = '__all__'
        exclude = ['company']
        
        widgets = {
            'member_welcome': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'loan_applied': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'loan_rejected': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'loan_approved': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'loan_cleared': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'loan_overdue': forms.Textarea(attrs={'class': 'form-control',  'required':'True', 'rows': 3, 'cols': 40}),
            'loan_balance': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
            'after_payment': forms.Textarea(attrs={'class': 'form-control', 'required':'True', 'rows': 3, 'cols': 40}),
        }