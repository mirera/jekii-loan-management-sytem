from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from branch.models import Branch
from loan.models import Loan, Repayment
from member.models import Member

@login_required(login_url='login')
def homepage(request):

    branches=Branch.objects.all()
    loans = Loan.objects.all()
    repayments = Repayment.objects.all()
    members= Member.objects.all()

    context= {'branches':branches, 'loans':loans, 'repayments':repayments, 'members':members }
    return render(request, 'index.html', context)
