from django import forms
from .models import Member, Branch

class MemberForm(forms.ModelForm):
    
    
    


    class Meta:
        model = Member
        fields = '__all__'
        exclude = [ 'date_joined']

  
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'id_no': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'phone_no': forms.NumberInput(attrs={'class': 'form-control','id': 'fv-email'}),
                'branch': forms.Select(attrs={'class': 'form-select js-select2'}),
                'business_name': forms.TextInput(attrs={'class': 'form-control'}),
                'industry': forms.Select(attrs={'class': 'form-select js-select2'}),
                'credit_score': forms.NumberInput(attrs={'class': 'form-control'}),
                'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your message'}),
                'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            } 
        
       

      