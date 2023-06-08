from django.db.models import Sum
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from loan.models import Collateral
from branch.models import Expense, ExpenseCategory
from loan.models import Loan, Repayment
from user.models import RecentActivity, Notification
from company.models import SmsSetting
from jekiiLMS.loan_math import loan_due_date, save_due_amount, get_previous_due_date , get_interval_period, update_credit_score, installments, total_payable_amount
from jekiiLMS.tasks import send_email_task, send_sms_task

'''
Run make sure this code runs after overdue_to_approved(loan)
This code updates due date once repayment made 
'''
def update_due_date(loan):
    sms_setting = SmsSetting.objects.get(company=loan.company)
    interval_period = get_interval_period(loan)
    last_due_date = get_previous_due_date(loan)
    current_date = timezone.now()
    payable_amount = total_payable_amount(loan)
    number_installments = installments(loan.loan_product)
    initial_due_amount = payable_amount / number_installments

    #handling case where borrower repays way ahead of more than one due date
    if last_due_date.date() > current_date.date():
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member,
            date_paid__date__lte=loan.due_date.date(),
            date_paid__date__gte=loan.approved_date.date()
        )
        total_repayments = repayments.aggregate(total_amount=Sum('amount'))['total_amount']

        #Number of elapsed intervals
        elapsed_intervals = (loan.due_date - loan.approved_date).days // interval_period 

        #Total expected due_amounts of elapsed repayment intervals
        expected_due_amounts = elapsed_intervals * initial_due_amount

        if total_repayments >= expected_due_amounts: 
            #update due date to new due date
            if loan.status == 'approved': 
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                loan.save()
            update_credit_score(loan)
        #at this point due amount as been updated for above 
        difference = total_repayments - expected_due_amounts 
        print(f'Before the loop {loan.due_amount}')
        
        #if the difference is >= initial due amount 
        while difference >= initial_due_amount:
            if loan.status == 'approved':
                #update due date to new due date
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                #update due amount
                loan.due_amount = loan.due_amount + initial_due_amount
                loan.save()
                print(f'Inside the loop {loan.due_amount}')
            update_credit_score(loan)  
            #difference = difference - loan.due_amount 
            difference = difference - initial_due_amount 
            if difference == 0:
                break

        if total_repayments >= loan.due_amount and loan.loan_balance() > 0:
            #send sms
            sender_id = sms_setting.sender_id
            token = sms_setting.api_token 
            message = f"Dear {loan.member.first_name}, You next payment is on {loan.due_date}. Success in your business."
            send_sms_task.delay(
                        sender_id, 
                        token, 
                        loan.member.phone_no, 
                        message
                    ) 
    #part 2a    
    else: #Handling a normal payment case
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member,
            date_paid__date__lte=current_date.date(),
            date_paid__date__gte=last_due_date.date()
        )
        total_repayments = repayments.aggregate(total_amount=Sum('amount'))['total_amount']
        if total_repayments >= loan.due_amount:
            #update due date to new due date
            if loan.status == 'approved': 
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                loan.save()
            update_credit_score(loan)

        #part 2b -- due amount is updated before this function is called on view
        difference = 0
        if loan.due_amount == 0:
            difference = 0
        elif loan.due_amount < 0:
            difference = loan.due_amount 
        
        #part 2c   
        while difference >= loan.due_amount:
            if loan.status == 'approved':
                #update due amount
                loan.due_amount = loan.due_amount + initial_due_amount

                #update due date to new due date
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                loan.save()

            update_credit_score(loan)  
            difference = difference - loan.due_amount
            if difference == 0:
                break
        #part 2d 
        # send message if due date is updated and loan is not cleared   
        if total_repayments >= loan.due_amount and loan.loan_balance() > 0:
            sender_id = sms_setting.sender_id
            token = sms_setting.api_token 
            message = f"Dear {loan.member.first_name}, You next payment is on {loan.due_date}. Success in your business."
            send_sms_task.delay(
                        sender_id, 
                        token, 
                        loan.member.phone_no, 
                        message
                    )   
  
# -- ends