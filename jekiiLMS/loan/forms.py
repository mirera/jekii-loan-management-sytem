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
            'minimum_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Minimum Loan Amount e.g 10000'}),
            'maximum_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Maximum Loan Amount e.g 50000'}),
            'loan_product_term': forms.NumberInput(attrs={'class': 'form-control','placeholder':'1,2,3..'}),
            'loan_term_period': forms.Select(attrs={'class': 'form-select js-select2'}),
            'repayment_frequency': forms.Select(attrs={'class': 'form-select js-select2', 'data-placeholder':'Select Term Period'}),   
            'interest_type': forms.Select(attrs={'class': 'form-select js-select2'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'20'}),
            'service_fee_type': forms.Select(attrs={'class': 'form-select js-select2'}),
            'service_fee_value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'10,20,30,...'}),
            'penalty_type': forms.Select(attrs={'class': 'form-select js-select2', 'id': 'pay-amount-1'}),
            'penalty_value': forms.NumberInput(attrs={'class': 'custom-control-input','placeholder':'20'}),
            'penalty_frequency': forms.Select(attrs={'class': 'form-select js-select2'}),
            'status': forms.Select(attrs={'class': 'form-select js-select2'}),
            'loan_product_description': forms.Textarea(attrs={'class': 'form-control form-control-sm','placeholder':'Describe your product....'}),
        }
