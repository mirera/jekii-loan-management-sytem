from celery import shared_task 
from django.utils import timezone
from loan.models import Loan, Repayment
from .loan_math import loan_due_date
from jekiiLMS.sms_messages import send_sms, send_email
from jekiiLMS.mpesa_api import disburse_loan

#task to mark a loan as overdue 
@shared_task
def mark_loans_as_overdue():
    #today = date.today()
    today = timezone.now()
    loans = Loan.objects.filter(due_date__lt=today).exclude(status__in=['cleared', 'overdue', 'written off', 'rolled over'])

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
            # send sms
            message = f"Dear {loan.member.first_name}, your loan installment of Ksh{loan.due_amount} is overdue. Make payment to avoid further penalties. Acc. 5840988 Paybill 522522"
            send_sms(loan.member.phone_no, message)

@shared_task
def hello_engima():
    print('I get printed after every minute')

#task to update due date 
@shared_task
def update_due_date():
    today = timezone.now()
    loans = Loan.objects.filter(due_date=today, status='approved') # run this every second or strp due date to date only
    for loan in loans:
        #get all repayment from approved_date to due_date
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member, 
            date_paid__lte=loan.due_date
        )

        total_repayments = sum(repayment.amount for repayment in repayments)
        amount_due = loan.amount_due()
        due_date_zof = loan.due_date.replace(tzinfo=None)

        if due_date_zof == today and total_repayments >= amount_due:
            # Change due date
            loan.due_date = loan_due_date(loan) 
            loan.save()

#task to send loan balances sms weekly
@shared_task
def send_loan_balance():
    loans = Loan.objects.filter(status__in=['approved', 'overdue'])
    
    for loan in loans:
        balance = loan.loan_balance()
        final_date = loan.final_payment_date().date().strftime('%Y-%m-%d')
        
        # send sms of loan balance
        message = f"Dear {loan.member.first_name}, Your current loan balance is Ksh{balance}. Final payment date is {final_date}. Wishing you success in your business."
        send_sms(loan.member.phone_no, message)
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

@shared_task
def print_message_task(message):
    # Call the send_sms function
    print(f'I am a product of Celery, {message}')


 