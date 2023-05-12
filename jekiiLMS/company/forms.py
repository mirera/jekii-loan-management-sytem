from dataclasses import fields
from django import forms
from .models import Organization, Package, SmsSetting


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
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'employees': forms.NumberInput(attrs={'class': 'form-control'}),
            #'date_added': forms.DateTimeInput(attrs={'class': 'form-control date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            'storage': forms.TextInput(attrs={'class': 'form-control', 'id': 'site-address'}),
        }

class SmsForm(forms.ModelForm):
    class Meta:
        model = SmsSetting
        fields = ['sender_id', 'api_token']
        
        widgets = {
            'sender_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'loginit'}),
            'api_token': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG'})
        }