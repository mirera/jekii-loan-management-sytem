from celery import shared_task 
from django.utils import timezone
from loan.models import Loan, Repayment
from company.models import SmsSetting
from .loan_math import update_due_amount,get_previous_due_date, update_credit_score
from .sms_messages import send_sms, send_email
from .mpesa_api import disburse_loan

#task to mark a loan as overdue 
@shared_task
def mark_loans_as_overdue():
    today = timezone.now()
    previous_due_date = get_previous_due_date(loan)
    # Find all loans that are due but not yet cleared or marked as overdue
    loans = Loan.objects.filter(due_date__lt=today).exclude(status__in=['cleared', 'overdue', 'written off', 'rolled over'])
    for loan in loans:
        # Check if there are any repayments made by the borrower for the loan
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member,
            date_paid__lte=today,
            date_paid__gt=previous_due_date
        )
        total_repayments = sum(repayment.amount for repayment in repayments)
        if total_repayments < loan.due_amount:
            # Loan is overdue
            loan.status = 'overdue'
            loan.save()

            #update member credit score
            update_credit_score(loan)

            # send sms
            message = f"Dear {loan.member.first_name}, your loan installment of Ksh{loan.due_amount} is overdue. Make payment to avoid further penalties. Acc. 5840988 Paybill 522522"
            sms_settings = SmsSetting.objects.get(company=loan.company)
            send_sms(sms_settings.sender_id, sms_settings.api_token, loan.member.phone_no, message)

@shared_task
def hello_engima():
    print('I get printed after every minute')

#update due amount foe overdue loans
@shared_task
def update_due_amount_task():
    loans = Loan.objects.filter(status='overdue')
    for loan in loans: 
        update_due_amount(loan)
# -- end --

#task to send loan balances sms weekly
@shared_task
def send_loan_balance():
    loans = Loan.objects.filter(status__in=['approved', 'overdue'])
    
    for loan in loans:
        balance = loan.loan_balance()
        final_date = loan.final_payment_date().date().strftime('%Y-%m-%d')
        
        # send sms of loan balance
        message = f"Dear {loan.member.first_name}, Your current loan balance is Ksh{balance}. Final payment date is {final_date}. Wishing you success in your business."
        sms_settings = SmsSetting.objects.get(company=loan.company)
        send_sms(sms_settings.sender_id, sms_settings.api_token, loan.member.phone_no, message)
# --end

@shared_task
def send_sms_task(sender_id, token, phone_number, message):
    # Call the send_sms function
    send_sms(sender_id, token, phone_number, message)

@shared_task
def send_email_task(context, template_path, from_name, from_email, subject, recipient_email, replyto_email):
    send_email(
        context, 
        template_path, 
        from_name, 
        from_email, 
        subject, 
        recipient_email, 
        replyto_email
    )

@shared_task
def disburse_loan_task(consumer_key, consumer_secret, shortcode, username, loan):
    disburse_loan(
        consumer_key, 
        consumer_secret, 
        shortcode, 
        username, 
        loan
    )




 