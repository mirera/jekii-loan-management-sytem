
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



#calculating loan amount to disbursw
def calculate_loan_amount(loan):
    member = loan.member
    loan_product = loan.loan_product
    credit_score = member.credit_score
    
    if credit_score < 5:
        return 0  # Member is flagged and doesn't qualify for a loan

    # Distribute the loan amount inside the credit score range
    amount_range = loan_product.maximum_amount - loan_product.minimum_amount
    amount_per_point = amount_range / 100
    amount_to_approve = loan_product.minimum_amount + (amount_per_point * credit_score)

    # Round the loan amount to the nearest hundred
    amount_to_approve = round(amount_to_approve / 100) * 100

    # Make sure the amount to approve is within the loan product's minimum and maximum amount
    amount_to_approve = max(loan_product.minimum_amount, min(loan_product.maximum_amount, amount_to_approve))
    if amount_to_approve > loan.applied_amount:
        amount_to_approve = loan.applied_amount
    else:
        amount_to_approve = amount_to_approve

    return amount_to_approve

#checking if collateral is sufficient
def is_sufficient_collateral(loan):
    recommended_amount = calculate_loan_amount(loan)
    required_collateral_value = recommended_amount * 3
    total_estimated_value = 0
    
    # Loop through all collaterals of the loan object
    collaterals = Collateral.objects.filter(loan=loan)
    if collaterals:
        for collateral in collaterals:
            total_estimated_value += collateral.estimated_value

        return total_estimated_value >= required_collateral_value
    else:
        return False

#calculate the amount to disburse 
def get_amount_to_disburse(loan, approved_amount): 
    service_fee_type = loan.loan_product.service_fee_type 
    service_fee_value = loan.loan_product.service_fee_value

    if approved_amount >= loan.loan_product.minimum_amount:
        if service_fee_type == 'fixed value':
            amount_to_disburse = approved_amount - service_fee_value
        elif service_fee_type == 'percentage':
            fee = approved_amount * service_fee_value * 0.01
            amount_to_disburse = approved_amount - fee
        return amount_to_disburse
    else:
        return 0 

#clear loan
def clear_loan(loan):
    loan_balance = loan.loan_balance()
    today = timezone.now()
    if loan_balance <= 0 and loan.status in ['approved', 'overdue', 'written off']:
                loan.status = 'cleared'
                loan.cleared_date = today 
                loan.save()
                
                loan.member.status = 'inactive'
                loan.member.save()
                #update member credit score
                update_credit_score(loan)

                # Create a recent activity entry for loan clearance
                RecentActivity.objects.create(
                    company = loan.company,
                    event_type='loan_clearance',
                    details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been cleared.'
                )
                Notification.objects.create(
                    company = loan.company,
                    recipient = loan.loan_officer,
                    state='success',
                    message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been cleared.'
                )
                #send sms
                sms_setting = SmsSetting.objects.get(company=loan.company)
                sender_id = sms_setting.sender_id
                token = sms_setting.api_token 
                message = f"Dear {loan.member.first_name}, You have successfully cleared your loan. Success in your business."
                send_sms_task.delay(
                            sender_id, 
                            token, 
                            loan.member.phone_no, 
                            message
                        ) 

#update member details after loan cleared               
def update_member_data(loan):
    if loan.status == 'cleared':
        member = loan.member
        member.previous_credit_score = member.credit_score
        #member.credit_score = member_credit_score(member)
        member.credit_score = update_credit_score(member)
        member.status = 'inactive'
        member.save() 
# -- ends

# -- write off a loan
def write_loan_off(loan):
    repayments = loan.repayments.all()
    total_repayments = repayments.aggregate(Sum('amount'))['amount__sum'] or 0
    amount = loan.total_payable() - total_repayments
    company = loan.company
    branch = loan.member.branch
    user_staff = User.objects.get(username=loan.loan_officer.username)
    if loan.status == 'overdue':
        # check if there is an expense category 'loan write offs'
        expense_category, _ = ExpenseCategory.objects.get_or_create(
            name='Loan Write Offs',
            company = company,
            defaults={'description': 'Expenses incurred due to loan write-offs.'}
        )
        
        # create an expense object with the above category
        expense = Expense.objects.create(
            company=company,
            amount=amount,
            category=expense_category,
            branch=branch,
            note=f"Loan write off for {loan}",
            expense_date=timezone.now(),
            created_by=user_staff,
        )
        
        # change loan status to written off and save loan
        loan.status = 'written off'
        loan.write_off_date = timezone.now()
        loan.write_off_expense = amount
        loan.save()

        #update member credit score to zero
        update_credit_score(loan)

        RecentActivity.objects.create(
            company = loan.company,
            event_type='loan_write_off',
            details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been written off.'
        )
        Notification.objects.create(
            company = loan.company,
            recipient = loan.loan_officer,
            state='stateless',
            message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been written off.'
        )
# -- ends

# --roll over loan
@transaction.atomic
def roll_over(loan):
    new_loan = Loan.objects.create(
        company = loan.company,
        loan_product= loan.loan_product,
        member= loan.member,
        applied_amount = loan.loan_balance(),
        application_date = loan.final_payment_date(),
        loan_officer = loan.loan_officer,
        loan_purpose = loan.loan_purpose,
        approved_amount = loan.loan_balance()
    )
    new_loan.disbursed_amount = loan.loan_balance()
    new_loan.num_installments = loan.num_installments
    new_loan.due_date = loan_due_date(new_loan)
    new_loan.disbursed_date = loan.final_payment_date()
    new_loan.approved_date = loan.final_payment_date()
    new_loan.approved_by = loan.approved_by
    new_loan.status = 'approved'
    new_loan.parent_loan = loan
    new_loan.save()

    # call fill due_amount function to fill due_amount on the Loan model 
    save_due_amount(new_loan)
    #old loan update
    loan.status = 'rolled over'
    loan.save()

    #update member credit score to zero
    update_credit_score(loan)

    RecentActivity.objects.create(
            company = loan.company,
            event_type='loan_roll_over',
            details=f'Loan of {loan.member.first_name} {loan.member.first_name} of {loan.approved_amount} has been rolled over.'
        )

    Notification.objects.create(
            company = loan.company,
            recipient = loan.loan_officer,
            state='stateless',
            message = f'Loan for {loan.member.first_name} {loan.member.last_name} has been rolled over.'
        )
    return new_loan
# -- ends

'''
The change_due_amount(loan) update loan due amount when a payment is made.
Do not confuse it with update_due_amount(loan) function.
'''
def change_due_amount(loan, repayment):
    if repayment.date_paid <= loan.due_date:
        loan.due_amount = loan.due_amount - int(repayment.amount)
        loan.save()


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
        total_repayments = repayments.aggregate(total_amount=Sum('amount'))['total_amount'] #10000
        print(f'total_repayments {total_repayments}')

        #Number of elapsed intervals 
        elapsed_intervals = (abs(loan.due_date - loan.approved_date) // interval_period) 
        print(loan.due_date)
        print(loan.approved_date)
        print(f'elapsed_intervals {elapsed_intervals}')
        #Total expected due_amounts of elapsed repayment intervals
        expected_due_amounts = elapsed_intervals * initial_due_amount #13000
        print(f'expected_due_amounts {expected_due_amounts}')


        if total_repayments >= expected_due_amounts: 
            #update due date to new due date
            print(f'Loan due date before manipulation {loan.due_date}')
            if loan.status == 'approved': 
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                loan.save()
                print(f'Loan due date after saving {loan.due_date}')
            update_credit_score(loan)
            #at this point due amount as been updated for above 
            difference = total_repayments - expected_due_amounts #-3000
            print(f'Difference {difference}')
            print(f'Loan balance {difference}')
            if loan.loan_balance() <= 0 : #False 6500
                #call clear loan function
                clear_loan(loan)
            else:
                if difference == 0: #borrower paid exact due amount
                    loan.due_amount = initial_due_amount
                elif difference < initial_due_amount: # borrower paid less due amount
                    loan.due_amount = initial_due_amount + loan.due_amount
                loan.save()

                print(f'Loan due amount before while loop {loan.due_amount}')
                print(f'Difference before while loop {difference}')
                
                #if the difference is >= initial due amount 
                while difference >= initial_due_amount:
                    if loan.status == 'approved':
                        #update due date to new due date
                        new_due_date = loan.due_date + interval_period  
                        loan.due_date = new_due_date
                        #update due amount
                        #loan.due_amount = loan.due_amount + initial_due_amount
                        if loan.due_amount == 0:
                            loan.due_amount = initial_due_amount
                        elif loan.due_amount < 0:
                            loan.due_amount = loan.due_amount + initial_due_amount
                        loan.save()
                        print(f'Inside the loop {loan.due_amount}')
                    update_credit_score(loan)  
                    #difference = difference - loan.due_amount 
                    difference = difference - initial_due_amount 
                    print(f'Difference after while loop {difference}')
                    if difference == 0:
                        break

                if total_repayments >= loan.due_amount and loan.loan_balance() > 0:
                    #send sms
                    sender_id = sms_setting.sender_id
                    token = sms_setting.api_token 
                    message = f"Dear {loan.member.first_name}, You next payment is on {loan.due_date.date()}. Due amount:{loan.due_amount} ."
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
        total_repayments = repayments.aggregate(total_amount=Sum('amount'))['total_amount'] #3250
        if total_repayments >= loan.due_amount: # true
            #update due date to new due date
            if loan.status == 'approved': #true
                new_due_date = loan.due_date + interval_period  
                loan.due_date = new_due_date
                loan.save()
                #due amount has been updated already
            update_credit_score(loan)

        #part 2b -- due amount is updated before this function is called on view
        difference = 0
        #case where borrower paid exact due amount
        if loan.due_amount == 0: 
            #update due amount 
            print(f'Before set to initial due amount {loan.due_amount}')
            loan.due_amount = initial_due_amount
            print(f'Before saving due amount already set to initial due amount {loan.due_amount}')
            loan.save()
        #case where borrower paid less than due amount
        elif loan.due_amount > 0: 
            #update due amount 
            loan.due_amount = initial_due_amount - loan.due_amount
            loan.save()
            #difference = 0
        #case where borrower paid more than due_amount
        elif loan.due_amount < 0: #-1000 test this part later
            difference = loan.due_amount
        
            #part 2c   
            while difference >= loan.due_amount:
                if loan.status == 'approved':
                    #update due amount
                    #loan.due_amount = loan.due_amount + initial_due_amount
                    if loan.due_amount == 0:
                        loan.due_amount = initial_due_amount
                    elif loan.due_amount < 0:
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
            message = f"Dear {loan.member.first_name}, You next payment is on {loan.due_date.date()}. Due amount:{loan.due_amount} ."
            send_sms_task.delay(
                        sender_id, 
                        token, 
                        loan.member.phone_no, 
                        message
                    )   
  
# -- ends

 
'''
Run this overdue_to_approved(loan) before you run update_due_date(loan)
Code changes loan status from overdue to approved if borrower clears due amount
'''
def overdue_to_approved(loan):
    if loan.status == 'overdue':
        #update member credit score before changing to approved
        update_credit_score(loan) 
        current_date = timezone.now()
        repayments = Repayment.objects.filter(
            loan_id=loan,
            member=loan.member,
            date_paid__lte=current_date,
            date_paid__gte= get_previous_due_date(loan)
        )
        total_repayments = repayments.aggregate(total_amount=Sum('amount'))['total_amount']
        if total_repayments >- loan.due_amount:
            loan.status = 'approved'
            loan.save()
