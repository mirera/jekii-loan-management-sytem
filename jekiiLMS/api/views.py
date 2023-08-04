from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import datetime
from django.utils import timezone
from rest_framework.decorators import api_view
from django.db.models.functions import TruncMonth
from member.models import Member
from .serializers import MemberSerializer
from loan.models import Loan
from branch.models import Branch
from .serializers import LoanSerializer, OrganizationSerializer, ExpenseSerializer, TemplateSettingSerializer, RoleSerializer
from company.models import Organization, TemplateSetting
from branch.models import Expense
from user.models import Role

@api_view(['GET']) 
def apiEndpoints(request):
    endpoints = {
        'Get all members':'http://127.0.0.1:8000/api/members',
        'Get all loans':'http://127.0.0.1:8000/api/loans',
        'Get a loan':'http://127.0.0.1:8000/api/loans',
        'Get expenses':'http://127.0.0.1:8000/api/expenses',
        'Get income':'http://127.0.0.1:8000/api/income',
        'Get income':'http://127.0.0.1:8000/api/companies',
        #company specific endpoints
        'Get company loans':'http://127.0.0.1:8000/api/loans/1',
        'Get company sms-templates':'http://127.0.0.1:8000/api/company/sms-templates/1',
        'Get company roles':'http://127.0.0.1:8000/api/company/roles/1',
        'Get company members':'http://127.0.0.1:8000/api/members/1',
        'Get company expenses':'http://127.0.0.1:8000/api/expenses/1',
        'Get company income-income':'http://127.0.0.1:8000/api/income-expense/1',
        'Get company loan perfomance':'http://127.0.0.1:8000/api/loans-repayment/1',
        'Get company loan dibursement':'http://127.0.0.1:8000/api/disbursement-data/1',

        #reports
        'Get company loans':'http://127.0.0.1:8000/api/company/reports/1/main-branch/30days',
    } 
    
    return Response(endpoints)

@api_view(['GET']) 
def getMembers(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def getLoans(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def getCompanies(request):
    companies = Organization.objects.all()
    serializer = OrganizationSerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCompanyLoans(request, company_id):
    loans = Loan.objects.filter(company=company_id)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCompanySmsTemplates(request, company_id):
    company = Organization.objects.get(id=company_id) 
    template_setting = TemplateSetting.objects.get(company=company)

    sms_templates = {
        "member_welcome": template_setting.member_welcome,
        "loan_applied": template_setting.loan_applied,
        "loan_rejected": template_setting.loan_rejected,
        "loan_approved": template_setting.loan_approved,
        "loan_cleared": template_setting.loan_cleared,
        "loan_overdue": template_setting.loan_overdue,
        "loan_balance": template_setting.loan_balance,
        "after_payment": template_setting.after_payment
    }

    return Response(sms_templates)

@api_view(['GET'])
def getCompanyRoles(request, company_id):
    company = Organization.objects.get(id=company_id) 
    roles = Role.objects.filter(company=company)
    roles_names = []

    for role in roles:
        roles_names.append(role.name)

    return Response(roles_names)

@api_view(['GET'])
def getCompanyMembers(request, company_id):
    members = Member.objects.filter(company=company_id)
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCompanyExpense(request, company_id):
    expense = Expense.objects.filter(company=company_id)
    serializer = ExpenseSerializer(expense, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCompanyIncomExpense(request, company_id):
    # Retrieve expenses for the given company and aggregate monthly expense data
    expense_data = Expense.objects.filter(company=company_id).annotate(
        expense_month=TruncMonth('expense_date')
    ).values('expense_month').annotate(total_expense=Sum('amount'))

    # Retrieve income data for the given company and aggregate monthly income data
    income_data = Loan.objects.filter(company=company_id, status__in=['cleared', 'rolled over']).annotate(
        income_month=TruncMonth('approved_date')
    ).values('income_month').annotate(total_income=Sum('interest_amount'))

    # Prepare the response data
    response_data = {
        'expenseData': [0] * 12,  # Initialize with 12 zeros
        'incomeData': [0] * 12,   # Initialize with 12 zeros
    }

    # Update the corresponding month's value in the response data
    for item in expense_data:
        month = item['expense_month'].month
        response_data['expenseData'][month - 1] = item['total_expense']

    for item in income_data:
        month = item['income_month'].month
        response_data['incomeData'][month - 1] = item['total_income']

    return Response(response_data)

'''
@api_view(['GET'])
def getCompanyIncomExpense(request, company_id):
    # Retrieve expenses for the given company and aggregate monthly expense data
    expense_data = Expense.objects.filter(company=company_id).values('expense_date__month').annotate(total_expense=Sum('amount'))

    # Retrieve income data for the given company and aggregate monthly income data
    income_data = Loan.objects.filter(company=company_id, status__in=['cleared','rolled over']).values('approved_date__month').annotate(total_income=Sum('interest_amount'))

    # Prepare the response data
    response_data = {
        'expenseData': [0] * 12,  # Initialize with 12 zeros
        'incomeData': [0] * 12,   # Initialize with 12 zeros
    }

    # Update the corresponding month's value in the response data
    for item in expense_data:
        month = item['expense_date__month']
        response_data['expenseData'][month - 1] = item['total_expense']

    for item in income_data:
        month = item['approved_date__month']
        response_data['incomeData'][month - 1] = item['total_income']

    return Response(response_data)
'''
@api_view(['GET']) 
def getCompanyLoansRepayments(request, company_id):
    today = datetime.now()
    mature_loans = Loan.objects.filter(final_due_date__lt=today, company=company_id) 
    amount_matured = mature_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    mature_cleared_loans = mature_loans.filter(status='cleared', )
    mature_cleared_amount = mature_cleared_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    defaulted_amount =  amount_matured - mature_cleared_amount 

    disbursed_loans = Loan.objects.filter(status__in=['approved','cleared','overdue']).filter(company=company_id)
    total_disbursed_amount = disbursed_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0
    immature_loan_amount = total_disbursed_amount - amount_matured

    data = [amount_matured, mature_cleared_amount, defaulted_amount, immature_loan_amount]

    return Response(data)

@api_view(['GET'])
def getCompanyLoansDisbursement(request, company_id):

    # Retrieve income data for the given company and aggregate monthly income data
    disbursement_data = Loan.objects.filter(company=company_id, status__in=['approved','cleared','overdue', 'written off', 'rolled over']).values('approved_date__month').annotate(total_count=Count('id'))

    # Prepare the response data
    response_data = {
        'disbursementData': [0] * 12,  # Initialize with 12 zeros
    }

    # Update the corresponding month's value in the response data

    for item in disbursement_data:
        month = item['approved_date__month']
        response_data['disbursementData'][month - 1] = item['total_count']

    return Response(response_data)


@api_view(['GET'])
def getCompanyLoansApplicationReports(request, company_id, branch_id, duration):
    
    # Retrieve the company based on the company_id
    try:
        company = Organization.objects.get(id=company_id)
    except:
        company = None

    #selected_branch
    selected_branch = request.POST.get('selected_branch')
    branch = Branch.objects.get(branch_name=selected_branch)

    current_date = timezone.now()

    #selected_duration
    selected_duration = request.POST.get('selected_duration')
    
    if selected_duration == '30 days':
        duration = 30
    elif selected_duration == '3 months':
        duration = 90
    elif selected_duration == '6 months':
        duration = 180
    elif selected_duration == '1 year':
        duration = 365
    elif selected_duration == 'Custom':
        duration = selected_duration #build the relativedelta object

    choosen_time = current_date - duration

    #get loan matching the query parameter
    if selected_branch == 'All branches': #handle case where the branch chosen is 'All branches'
        loans = Loan.objects.filter(company=company,application_date__lte=choosen_time) #for all branches
    else:
        loans = Loan.objects.filter(company=company, branch=branch, application_date__lte=choosen_time)  

    response_data = {
        
    }   
    
    return Response(response_data)