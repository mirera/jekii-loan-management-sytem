from dataclasses import fields
from django import forms
from .models import Organization, Package, SmsSetting, MpesaSetting, EmailSetting


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['admin', 'date_joined']
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id':'customFile', 'type':'file'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'site-address'}),
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
        fields = ['sender_id', 'api_token']
        
        widgets = {
            'sender_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'loginit', 'required':'True'}),
            'api_token': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG', 'required':'True'})
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