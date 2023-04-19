from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import Branch, ExpenseCategory, Expense


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        exclude = ['status', 'company']
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'open_date': forms.DateTimeInput(attrs={'class': 'form-control date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            'capital': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pay-amount-1'}),
            #'status': forms.Select(attrs={'class': 'custom-control-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your message'}),
        }


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Describe the category..'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ['created_by']
        
        
        widgets = {
            'expense_date': forms.DateInput(attrs={'class': 'form-control date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            'category': forms.Select(attrs={'class': 'form-select js-select2'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pay-amount-1'}),
            'branch': forms.Select(attrs={'class': 'form-select js-select2'}),
            'note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your message'}),
            'attachement': forms.FileInput(attrs={'class': 'form-control'}),
        }