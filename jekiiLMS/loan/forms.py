from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import LoanProduct


class LoanProductForm(forms.ModelForm):
    class Meta:
        model = LoanProduct
        fields = '__all__'
        
        
        widgets = {
            'loan_product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'minimum_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'maximum_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan_product_term': forms.NumberInput(attrs={'class': 'form-control','placeholder':'1,2,3..'}),
            'loan_term_period': forms.Select(attrs={'class': 'form-control'}),
            'repayment_frequency': forms.Select(attrs={'class': 'form-control'}),
            'interest_type': forms.Select(attrs={'class': 'form-control'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'20'}),
            'service_fee_type': forms.Select(attrs={'class': 'form-control'}),
            'service_fee_value': forms.NumberInput(attrs={'class': 'form-control date-picker', 'data-date-format':'yyyy-mm-dd'}),
            'penalty_type': forms.Select(attrs={'class': 'form-control', 'id': 'pay-amount-1'}),
            'penalty_value': forms.NumberInput(attrs={'class': 'custom-control-input','placeholder':'20'}),
            'penalty_frequency': forms.Select(attrs={'class': 'custom-control-input'}),
            'status': forms.Select(attrs={'class': 'custom-control-input'}),
            'loan_product_description': forms.Textarea(attrs={'class': 'form-control form-c,ntrol-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your Description'}),
        }
