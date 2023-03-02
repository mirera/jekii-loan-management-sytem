from django import forms
from .models import Member, Branch

class MemberForm(forms.ModelForm):
    
    branch = forms.ModelChoiceField(queryset=Branch.objects.all().order_by('open_date'))

    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['credit_score', 'date_joined']
  
    widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control','id': 'fv-email'}),
            'branch': forms.Select(attrs={'class': 'form-select js-select2'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.Select(attrs={'class': 'form-select js-select2'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Write your message'}),
            'passport_photo': forms.FileInput(attrs={'class': 'custom-control-input'}),
        }

    def save(self, commit=True):
        member = super().save(commit=False)
        branch_id = self.cleaned_data.get('branch')
        branch = Branch.objects.get(id=branch_id)
        member.branch = branch
        if commit:
            member.save()
        return member