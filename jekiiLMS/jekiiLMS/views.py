from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from branch.models import Branch, Expense
from loan.models import Loan, Repayment
from member.models import Member
from company.models import Company


 #--- superadmin dashboard  logic starts here---
@login_required(login_url='login')
def superadmin_dashboard(request): 

    #companies=Company.objects.all()
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
        'branches':branches, 
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


#--- staff dashboard logic starts here---  
@login_required(login_url='login')
def staff_dashboard(request): 

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
        'branches':branches, 
        'loans':loans, 
        'repayments':repayments,
        'members':members,
        'total_pending_loans':total_pending_loans,
        'total_pending_amount':total_pending_amount,
        'total_disbursed_amount':total_disbursed_amount,
        'expense':expense
        }
    return render(request, 'staff-dash.html', context)
  #--- staff dashboard logic ends here---

#--- companyadmin dashboard logic starts here---  
@login_required(login_url='login')
def homepage(request): 

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
        'branches':branches, 
        'loans':loans, 
        'repayments':repayments,
        'members':members,
        'total_pending_loans':total_pending_loans,
        'total_pending_amount':total_pending_amount,
        'total_disbursed_amount':total_disbursed_amount,
        'expense':expense
        }
    return render(request, 'index.html', context)
  #--- companyadmin dashboard logic ends here---