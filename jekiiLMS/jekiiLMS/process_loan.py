
from django.db.models import Sum
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from loan.models import Collateral
from branch.models import Expense, ExpenseCategory
from loan.models import Loan
from user.models import RecentActivity, Notification
from company.models import SmsSetting
from .credit_score import member_credit_score, update_credit_score
from jekiiLMS.sms_messages import send_sms
from jekiiLMS.loan_math import loan_due_date, save_due_amount, installments
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
    company = loan.company
    loanproduct = loan.loan_product
    member = loan.member
    applied_amount = loan.loan_balance()
    final_payment_date = loan.final_payment_date()
    loan_officer = loan.loan_officer
    purpose = loan.loan_purpose
    admin = loan.approved_by


    new_loan = Loan.objects.create(
        company = company,
        loan_product= loanproduct,
        member= member,
        applied_amount = applied_amount,
        application_date = final_payment_date,
        loan_officer = loan_officer,
        loan_purpose = purpose,
        approved_amount = applied_amount
    )
    new_loan.disbursed_amount = get_amount_to_disburse(new_loan, applied_amount)
    new_loan.num_installments = installments(new_loan.loan_product)
    new_loan.due_date = loan_due_date(new_loan)
    new_loan.disbursed_date = final_payment_date
    new_loan.approved_date = final_payment_date
    new_loan.approved_by = admin
    new_loan.status = 'approved'
    new_loan.parent_loan = loan
    new_loan.save()

    # call fill due_amount function to fill due_amount on the Loan model 
    save_due_amount(new_loan)
    #old loan update
    loan.status = 'rolled over'
    loan.save()

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


