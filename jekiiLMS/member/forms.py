from django import forms
from .models import Member, Branch

class MemberForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all().order_by('name'))

    class Meta:
        model = Member
        #fields = ['name', 'branch']
        fields = '__all__'
