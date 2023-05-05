from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from branch.models import Branch, Expense
from loan.models import Loan, Repayment
from member.models import Member
from company.models import Organization
from user.models import CompanyStaff



 #--- superadmin dashboard  logic starts here---
@login_required(login_url='login')
def superadmin_dashboard(request): 

    companies=Organization.objects.all()
    active_companies = Organization.objects.filter(status='active')
    license_expired_companies = Organization.objects.filter(is_license_expired=True)
    branches=Branch.objects.all()
    loans = Loan.objects.all()
    repayments = Repayment.objects.all()
    members= Member.objects.all()

    pending_loans = Loan.objects.filter(status ='pending')
    total_pending_loans = pending_loans.count()
    total_pending_amount = pending_loans.aggregate(Sum('applied_amount'))['applied_amount__sum'] or 0

    disbursed_loans = Loan.objects.filter(status ='approved')
    total_disbursed_amount = disbursed_loans.aggregate(Sum('applied_amount'))['applied_amount__sum'] or 0

    total_expense = Expense.objects.all()
    expense = total_expense.aggregate(Sum('amount'))['amount__sum'] or 0

    context= {
        'companies':companies,
        'active_companies':active_companies,
        'license_expired_companies':license_expired_companies, 
        'loans':loans, 
        'repayments':repayments,
        'members':members,
        'total_pending_loans':total_pending_loans,
        'total_pending_amount':total_pending_amount,
        'total_disbursed_amount':total_disbursed_amount,
        'expense':expense
        }
    return render(request, 'superadmin-dash.html', context)
  #--- superadmin dashboard logic ends here---


#--- companyadmin dashboard logic starts here---  
@login_required(login_url='login')
def homepage(request): 


    branches=Branch.objects.all()
    loans = Loan.objects.all()
    repayments = Repayment.objects.all()
    members= Member.objects.all()

    #company staff context
    staff = CompanyStaff.objects.get(username=request.user.username)

    #disbursed loans contexts
    disbursed_loans = Loan.objects.filter(status__in=['approved','cleared','overdue'])
    num_disbursed_loans = disbursed_loans.count()
    total_disbursed_amount = disbursed_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0
    #disbursed loans contexts - staff specific
    staff_disbursed_loans = Loan.objects.filter(status__in=['approved','cleared','overdue']).filter(loan_officer=staff)
    staff_num_disbursed_loans = staff_disbursed_loans.count()
    staff_total_disbursed_amount = staff_disbursed_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    #pending loans contexts
    pending_loans = Loan.objects.filter(status ='pending')
    total_pending_loans = pending_loans.count()
    total_pending_amount = pending_loans.aggregate(Sum('applied_amount'))['applied_amount__sum'] or 0
    #pending loans contexts - staff specific
    staff_pending_loans = Loan.objects.filter(status ='pending', loan_officer=staff)
    staff_num_pending_loans = staff_pending_loans.count()
    staff_total_pending_amount = staff_pending_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0


    #overdue loans contexts
    overdue_loans = Loan.objects.filter(status ='overdue')
    total_overdue_loans = overdue_loans.count()
    total_overdue_amount = overdue_loans.aggregate(Sum('due_amount'))['due_amount__sum'] or 0
    #overdue loans contexts - staff specific
    staff_overdue_loans = Loan.objects.filter(status ='overdue', loan_officer=staff)
    staff_num_overdue_loans = staff_overdue_loans.count()
    staff_total_overdue_amount = staff_overdue_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    #expenses contexts
    total_expense = Expense.objects.all()
    expense = total_expense.aggregate(Sum('amount'))['amount__sum'] or 0
    #expenses contexts - staff specific
    staff_total_expense = Expense.objects.filter(created_by=request.user)
    staff_expense = staff_total_expense.aggregate(Sum('amount'))['amount__sum'] or 0

    context= {
        'branches':branches, 
        'loans':loans, 
        'repayments':repayments,
        'members':members,
        'staff':staff,
        'total_pending_loans':total_pending_loans,
        'total_pending_amount':total_pending_amount,
        'staff_num_pending_loans':staff_num_pending_loans,
        'staff_total_pending_amount':staff_total_pending_amount,
        'num_disbursed_loans':num_disbursed_loans,
        'total_disbursed_amount':total_disbursed_amount,
        'staff_num_disbursed_loans':staff_num_disbursed_loans,
        'staff_total_disbursed_amount':staff_total_disbursed_amount,
        'total_overdue_loans':total_overdue_loans,
        'total_overdue_amount':total_overdue_amount,
        'staff_num_overdue_loans':staff_num_overdue_loans,
        'staff_total_overdue_amount':staff_total_overdue_amount,
        'expense':expense,
        'staff_expense':staff_expense
        }
    return render(request, 'index.html', context)
  #--- companyadmin dashboard logic ends here--- 