from dataclasses import fields
from django import forms
from .models import LoanProduct, Loan, Repayment, Guarantor, Collateral, MpesaStatement
from member.models import Member
from user.forms import CompanyStaff


class LoanProductForm(forms.ModelForm): 
    class Meta:
        model = LoanProduct
        fields = '__all__'
        
        
        widgets = {
            'loan_product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Product Name'}),
            'minimum_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Minimum Loan Amount e.g 10000'}),
            'maximum_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Maximum Loan Amount e.g 50000'}),
            'loan_product_term': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter the loan term e.g 3'}),
            'loan_term_period': forms.Select(attrs={'class': 'form-select js-select2'}),
            'repayment_frequency': forms.Select(attrs={'class': 'form-select js-select2'}),   
            'interest_type': forms.Select(attrs={'class': 'form-select js-select2'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Interest rate e.g 3 without %'}),
            'service_fee_type': forms.Select(attrs={'class': 'form-select js-select2'}),
            'service_fee_value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'10,20,30,...'}),
            'penalty_type': forms.Select(attrs={'class': 'form-select js-select2', 'id': 'pay-amount-1'}),
            'penalty_value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter penalty value/rate e.g 20'}),
            'penalty_frequency': forms.Select(attrs={'class': 'form-select js-select2'}),
            'status': forms.Select(attrs={'class': 'form-select js-select2'}),
            'loan_product_description': forms.Textarea(attrs={'class': 'form-control form-control-sm','placeholder':'Write a short description of your product.'}),
        }

class LoanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)  # Get the company from kwargs, set default to None
        super(LoanForm, self).__init__(*args, **kwargs)
        self.fields['loan_product'].queryset = LoanProduct.objects.filter(company=company)
        self.fields['member'].queryset = Member.objects.filter(company=company, status='inactive')
        self.fields['loan_officer'].queryset = CompanyStaff.objects.filter(company=company, status='active').exclude(user_type='admin')

        # Disable the loan_id field in the edit form
        var = self.fields['loan_id']
        var.disabled = True

    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['approved_amount', 'disbursed_amount','disbursed_date',
                    'cleared_date', 'approved_date', 'approved_by',
                     'amount_mpesa_s',
                    ]

        widgets = {
            'loan_id': forms.TextInput(attrs={'class': 'form-control' }),
            'loan_product': forms.Select(attrs={'class': 'form-select js-select2'}),
            'member': forms.Select(attrs={'class': 'form-select js-select2'}),
            'applied_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'1000'}),
            'application_date': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            'loan_officer': forms.Select(attrs={'class': 'form-select js-select2'}),
            'status': forms.Select(attrs={'class': 'form-select js-select2'}),
            'loan_purpose': forms.Textarea(attrs={'class': 'form-control form-control-sm',
                                                 'id': 'cf-default-textarea' ,'placeholder':'Write loan purpose'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'})
        }

class RepaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)  # Get the company from kwargs, set default to None
        super(RepaymentForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(company=company, status='active')

    class Meta:
        model = Repayment
        fields = '__all__'
        exclude = ['loan_id', 'company']
        
        
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            #'loan_id': forms.Select(attrs={'class': 'form-select js-select2'}),
            'member': forms.Select(attrs={'class': 'form-select js-select2'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'1000'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control date-picker-range', 'data-date-format':'yyyy-mm-dd'}),   
            
        } 

class GuarantorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)  # Get the company from kwargs, set default to None
        borrower = kwargs.pop('borrower', None)  # Get the borrower from kwargs, set default to None
        super(GuarantorForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Member.objects.filter(company=company, status='inactive').exclude(id=borrower.id)


    class Meta:
        model = Guarantor
        fields = '__all__'
        exclude = ['created']
        widgets = {
            #'loan': forms.Select(attrs={'class': 'form-select js-select2'}),
            'name': forms.Select(attrs={'class': 'form-select js-select2'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000'})      
        }
 
class CollateralForm(forms.ModelForm):
    class Meta:
        model = Collateral
        fields = '__all__'
        
        
        widgets = {
            'loan': forms.Select(attrs={'class': 'form-select js-select2'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Samsung 41 TV'}),
            'type': forms.Select(attrs={'class': 'form-select js-select2'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'30000'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'0123-W239'})
        } 
  
class MpesaStatementForm(forms.ModelForm):
    class Meta:
        model = MpesaStatement
        fields = ['statements', 'code']
        
        
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control','placeholder':'1234'}),
            'statements': forms.FileInput(attrs={'class': 'form-control'})
        } 
  
 