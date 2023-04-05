from dataclasses import fields
from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['admin', 'date_joined']
        
        
        widgets = {
            #'admin': forms.Select(attrs={'class': 'custom-control-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id':'customFile', 'type':'file'}),
            #'date_joined': forms.DateTimeInput(attrs={'class': 'form-control date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'site-address'}),
        }