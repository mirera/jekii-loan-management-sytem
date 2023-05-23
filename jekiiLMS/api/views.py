from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import datetime
from rest_framework.decorators import api_view
from member.models import Member
from .serializers import MemberSerializer
from loan.models import Loan
from .serializers import LoanSerializer, OrganizationSerializer, ExpenseSerializer
from company.models import Organization
from branch.models import Expense


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
        'Get company members':'http://127.0.0.1:8000/api/members/1',
        'Get company expenses':'http://127.0.0.1:8000/api/expenses/1',
        'Get company income-income':'http://127.0.0.1:8000/api/income-expense/1',
        'Get company loan perfomance':'http://127.0.0.1:8000/api/loans-repayment/1',
        'Get company loan dibursement':'http://127.0.0.1:8000/api/disbursement-data/1',
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