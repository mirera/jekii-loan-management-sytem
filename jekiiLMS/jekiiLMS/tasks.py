from celery import shared_task 
from django.utils import timezone
from datetime import timedelta
from loan.models import Loan, Repayment
from company.models import SmsSetting, SystemSetting, TemplateSetting
from .loan_math import update_due_amount,get_previous_due_date, update_credit_score, total_penalty,get_interval_period
from .sms_messages import send_sms, send_email
from .mpesa_api import disburse_loan 

#task to mark a loan as overdue 
@shared_task
def mark_loans_as_overdue():
    today = timezone.now().date()
    
    # Find all loans that are due but not yet cleared or marked as overdue
    loans = Loan.objects.filter(due_date__date__lt=today).exclude(status__in=['cleared', 'overdue', 'written off', 'rolled over'])
    for loan in loans:
        previous_due_date = get_previous_due_date(loan).date()
        # Check if there are any repayments made by the borrower for the loan
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member,
            date_paid__lte=today,
            date_paid__gt=previous_due_date
        )
        total_repayments = sum(repayment.amount for repayment in repayments)

        #include a case of mutiple missed payments
        start_date = loan.approved_date + timedelta(days=1)
        interval_period = get_interval_period(loan) #in timedelta(days=50) format
        difference = (timezone.now() - start_date).days ##get difference between start date and current_date
        expired_intervals = difference // interval_period.days #get expired payment intervals/installments
        penalities = total_penalty(loan)
        if penalities is None:
            penalities = 0
        missed_payments = expired_intervals * loan.due_amount + penalities

        if total_repayments < missed_payments:
        #if total_repayments < loan.due_amount:
            # Loan is overdue
            loan.status = 'overdue'
            loan.save()
            #update member credit score
            update_credit_score(loan)

            try:
                system_settings = SystemSetting.objects.get(company=loan.company)
            except SystemSetting.DoesNotExist:
                system_settings = None

            try:
                sms_settings = SmsSetting.objects.get(company=loan.company)
            except SmsSetting.DoesNotExist:
                sms_settings = None
            
            try:
                template_setting = TemplateSetting.objects.get(company=loan.company)
            except:
                template_setting = None

            #available tags 
            first_name = loan.member.first_name
            last_name = loan.member.last_name
            organization_name = loan.member.company.name
            currency = loan.company.currency
            due_amount = loan.due_amount 
            account_no = loan.company.account_no
            paybill_no = loan.company.paybill_no

            #format raw message template 
            message_raw = template_setting.loan_overdue 
            message = message_raw.format(
                first_name=first_name, 
                last_name=last_name, 
                organization_name=organization_name, 
                currency=currency,
                due_amount=due_amount,
                account_no=account_no,
                paybill_no=paybill_no,
            )

            if sms_settings is not None:
                if system_settings.is_send_sms and sms_settings.api_token is not None and sms_settings.sender_id is not None:
                    # send sms
                    send_sms(
                        sms_settings.sender_id, 
                        sms_settings.api_token, 
                        loan.member.phone_no, 
                        message
                    )

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

        try:
            system_settings = SystemSetting.objects.get(company=loan.company)
        except SystemSetting.DoesNotExist:
            system_settings = None

        try:
            sms_settings = SmsSetting.objects.get(company=loan.company)
        except SmsSetting.DoesNotExist:
            sms_settings = None
        try:
            template_setting = TemplateSetting.objects.get(company=loan.company)
        except:
            template_setting = None

        #available tags 
        first_name = loan.member.first_name
        last_name = loan.member.last_name
        organization_name = loan.member.company.name
        currency = loan.company.currency
        due_date = loan.due_date.date().strftime('%Y-%m-%d')
        due_amount = loan.due_amount 
        loan_balance = balance
        account_no = loan.company.account_no
        paybill_no = loan.company.paybill_no

        #format raw message template 
        message_raw = template_setting.loan_balance 
        message = message_raw.format(
            first_name=first_name, 
            last_name=last_name, 
            organization_name=organization_name, 
            currency=currency,
            due_date=due_date,
            due_amount=due_amount,
            loan_balance=loan_balance,
            account_no=account_no,
            paybill_no=paybill_no,
            final_date=final_date
        )
        
        if sms_settings is not None:
            if system_settings.is_send_sms and sms_settings.api_token is not None and sms_settings.sender_id is not None:
                # send sms of loan balance
                send_sms(
                    sms_settings.sender_id, 
                    sms_settings.api_token, 
                    loan.member.phone_no, 
                    message)
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




 