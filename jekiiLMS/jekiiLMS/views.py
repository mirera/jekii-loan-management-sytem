from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required 
from branch.models import Branch, Expense
from loan.models import Loan, Repayment
from member.models import Member
from company.models import Organization
from user.models import CompanyStaff
from user.models import RecentActivity



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
    if request.user.is_authenticated and request.user.is_active:
              try:
                  companystaff = CompanyStaff.objects.get(username=request.user.username)
                  company = companystaff.company
              except CompanyStaff.DoesNotExist:
                  company = None
    else:
              company = None
 
    branches=Branch.objects.filter(company=company)
    loans = Loan.objects.filter(company=company).order_by('-application_date')[:5]
    repayments = Repayment.objects.filter(company=company)
    members= Member.objects.filter(company=company).order_by('-date_joined')[:5]
    today = datetime.now()

    recent_activities = RecentActivity.objects.order_by('-timestamp')[:5]

    #company staff context
    staff = CompanyStaff.objects.get(username=request.user.username)

    all_loans = Loan.objects.all().count()
    #rejected loans contexts
    rejected_loans = Loan.objects.filter(status='rejected').filter(company=company)
    num_rejected_loans = rejected_loans.count()
    pc_rejected_loans = round(num_rejected_loans * 100 /all_loans , 2)

    #rolledover loans contexts
    rolledover_loans = Loan.objects.filter(status='rolled over').filter(company=company)
    num_rolledover_loans = rolledover_loans.count()
    pc_rolled_loans = round(num_rolledover_loans * 100 /all_loans , 2)

    #disbursed loans contexts
    disbursed_loans = Loan.objects.filter(status__in=['approved','cleared','overdue', 'written off', 'rolled over']).filter(company=company)
    num_disbursed_loans = disbursed_loans.count()
    pc_disbursed_loans = round(num_disbursed_loans * 100 /all_loans , 2)
    total_disbursed_amount = disbursed_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    #disbursed loans contexts - staff specific
    staff_disbursed_loans = Loan.objects.filter(status__in=['approved','cleared','overdue']).filter(loan_officer=staff, company=company)
    staff_num_disbursed_loans = staff_disbursed_loans.count()
    staff_total_disbursed_amount = staff_disbursed_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    #pending loans contexts
    pending_loans = Loan.objects.filter(status ='pending', company=company)
    total_pending_loans = pending_loans.count()
    total_pending_amount = pending_loans.aggregate(Sum('applied_amount'))['applied_amount__sum'] or 0
    #pending loans contexts - staff specific
    staff_pending_loans = Loan.objects.filter(status ='pending', loan_officer=staff, company=company)
    staff_num_pending_loans = staff_pending_loans.count()
    staff_total_pending_amount = staff_pending_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0


    #overdue loans contexts
    overdue_loans = Loan.objects.filter(status ='overdue', company=company)
    total_overdue_loans = overdue_loans.count()
    total_overdue_amount = overdue_loans.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

    #overdue loans contexts - staff specific
    staff_overdue_loans = Loan.objects.filter(status ='overdue', loan_officer=staff, company=company)
    staff_num_overdue_loans = staff_overdue_loans.count()
    staff_total_overdue_amount = staff_overdue_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    #expenses contexts
    total_expense = Expense.objects.filter(company=company)
    expense = total_expense.aggregate(Sum('amount'))['amount__sum'] or 0
    #expenses contexts - staff specific
    staff_total_expense = Expense.objects.filter(created_by=request.user, company=company)
    staff_expense = staff_total_expense.aggregate(Sum('amount'))['amount__sum'] or 0

    #mature loan contexts
    mature_loans = Loan.objects.filter(final_due_date__lt=today, company=company) 
    amount_matured = mature_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0
    if total_disbursed_amount != 0:
        matured_pc = round(amount_matured * 100 / total_disbursed_amount, 2)
    else:
        matured_pc = 0
    

    # mature cleared contexts
    mature_cleared_loans = mature_loans.filter(status='cleared', )
    mature_cleared_amount = mature_cleared_loans.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0

    if total_disbursed_amount != 0:
        mature_cleared_pc = round(mature_cleared_amount * 100 / total_disbursed_amount, 2)
    else:
        mature_cleared_pc = 0

    #immature loans
    immature_loan_amount = total_disbursed_amount - amount_matured

    if total_disbursed_amount != 0:
        immature_pc = round(immature_loan_amount * 100 / total_disbursed_amount, 2)
    else:
        immature_pc = 0

    #mature defaulted context
    defaulted_amount =  amount_matured - mature_cleared_amount 
    if total_disbursed_amount != 0:
        defaulted_pc = round(defaulted_amount * 100 / total_disbursed_amount, 2)
    else:
        defaulted_pc = 0

    # income, service fees, penalties secured contexts
    interest_secured = mature_cleared_loans.aggregate(Sum('interest_amount'))['interest_amount__sum'] or 0 
    service_fee = mature_cleared_loans.aggregate(Sum('service_fee_amount'))['service_fee_amount__sum'] or 0 
    total_income = interest_secured + service_fee #later add penalty secured 

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
        'staff_expense':staff_expense,
        'amount_matured':amount_matured,
        'immature_loan_amount':immature_loan_amount,
        'mature_cleared_amount':mature_cleared_amount,
        'defaulted_amount':defaulted_amount,
        'total_income':total_income,
        'mature_cleared_pc':mature_cleared_pc,
        'matured_pc':matured_pc,
        'immature_pc':immature_pc,
        'defaulted_pc':defaulted_pc,
        'num_rolledover_loans':num_rolledover_loans,
        'num_rejected_loans':num_rejected_loans,
        'pc_rejected_loans':pc_rejected_loans,
        'pc_rolled_loans':pc_rolled_loans,
        'pc_disbursed_loans':pc_disbursed_loans,
        'recent_activities':recent_activities,
        }
    return render(request, 'index.html', context)
  #--- companyadmin dashboard logic ends here--- 