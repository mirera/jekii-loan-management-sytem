from celery import shared_task
from datetime import date
from loan.models import Loan, Repayment

@shared_task
def mark_loans_as_overdue():
    today = date.today()
    overdue_loans = []
    loans = Loan.objects.filter(next_payment_date__lt=today).exclude(status__in=['cleared', 'overdue'])

    # Find all loans that are due but not yet cleared or marked as overdue
    for loan in loans:
        # Check if there are any repayments made by the borrower for the loan
        repayments = Repayment.objects.filter(loan_id=loan.id, member=loan.member)
        total_repayments = sum(repayment.amount for repayment in repayments)
        total_payable = loan.total_payable()
        if total_repayments < total_payable:
            # Loan is overdue
            loan.status = 'overdue'
            loan.save()
            overdue_loans.append(loan)