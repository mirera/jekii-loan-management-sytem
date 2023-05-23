
from django import forms
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError  
from .models import CompanyStaff
from branch.models import Branch
from user.models import Role
from django.forms.widgets import CheckboxSelectMultiple


class CustomUserCreationForm(forms.Form): 
    company_name = forms.CharField(label='Enter Company Name')
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class CompanyStaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)  # Get the company from kwargs, set default to None
        super(CompanyStaffForm, self).__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.objects.filter(company=company)
        self.fields['staff_role'].queryset = Role.objects.filter(company=company)

    class Meta:
        model = CompanyStaff 
        fields = '__all__'


  
        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your first name'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Enter password','type':'password', 'id':'password'}), #on edit make the password not visible
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your first name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your last name'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'id_no': forms.TextInput(attrs={'class': 'form-control', 'minlength':'8'}),
                'phone_no': forms.NumberInput(attrs={'class': 'form-control','id': 'fv-email', 'placeholder':'0712345678', 'minlength':'10'}),
                'branch': forms.Select(attrs={'class': 'form-select js-select2'}), 
                'user_type': forms.Select(attrs={'class': 'form-select js-select2'}),
                'staff_role': forms.Select(attrs={'class': 'form-select js-select2'}),
                'status': forms.Select(attrs={'class': 'form-select js-select2'}),
                'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
                
            } 
        
class RoleForm(forms.Form):

    name = forms.CharField(
        label='Role Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    permissions = forms.ModelMultipleChoiceField(
        label='Permissions',
        queryset=Permission.objects.filter(
            content_type__model__in=['branch', 'expensecategory', 'expense',
             'member','loanproduct', 'loan', 'repayment','collateral', 'guarantor',
             'companyadmin', 'companystaff', 'role', 'note' ]  # Filter by models you want
        ),
        widget=CheckboxSelectMultiple(attrs={'class': 'custom-class d-inline'}),
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
    )

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].label_from_instance = self.label_from_permission

    def label_from_permission(self, obj):
        return obj.name
