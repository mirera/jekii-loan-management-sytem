from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'open_date': forms.DateTimeInput(attrs={'class': 'form-control date-picker', 'data-date-format':'yyyy-mm-dd'}),
            'capital': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pay-amount-1'}),
            'status': forms.Select(attrs={'class': 'custom-control-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your message'}),
        }
