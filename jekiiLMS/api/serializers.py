from rest_framework import serializers
from member.models import Member
from loan.models import Loan
from company.models import Organization, TemplateSetting
from branch.models import Expense


class MemberSerializer(serializers.ModelSerializer):
     class Meta: 
        model = Member
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
     class Meta:
        model = Loan
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Organization
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
     class Meta:
        model = Expense
        fields = '__all__'

class TemplateSettingSerializer(serializers.ModelSerializer):
     class Meta:
        model = TemplateSetting
        fields = '__all__'