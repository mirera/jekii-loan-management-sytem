from django import forms
from .models import Member, Branch

class MemberForm(forms.ModelForm):
    
    
    


    class Meta:
        model = Member
        fields = '__all__'


  
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your first name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your last name'}),
                'id_no': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'phone_no': forms.NumberInput(attrs={'class': 'form-control','id': 'fv-email', 'placeholder':'0712345678'}),
                'branch': forms.Select(attrs={'class': 'form-select js-select2'}),
                'business_name': forms.TextInput(attrs={'class': 'form-control'}),
                'industry': forms.Select(attrs={'class': 'form-select js-select2'}),
                'credit_score': forms.NumberInput(attrs={'class': 'form-control'}),
                'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Location of business..'}),
                'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
                'date_joined': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd'}),
            } 
        
       

      