from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone 
import math

# loan paymnent interval period
def get_interval_period(loan):
    if loan.loan_product.repayment_frequency == 'onetime':
        # For one-time payments, the due date is simply the application date plus the loan product term
        if loan.loan_product.loan_term_period == 'day':
            interval_period = timedelta(days=loan.loan_product.loan_product_term)
        elif loan.loan_product.loan_term_period == 'week':
            interval_period = timedelta(days=loan.loan_product.loan_product_term * 7)
        elif loan.loan_product.loan_term_period == 'month':
            interval_period = timedelta(days=loan.loan_product.loan_product_term * 30)
        else:
            interval_period = timedelta(days=loan.loan_product.loan_product_term * 365)
    elif loan.loan_product.repayment_frequency == 'daily':
        interval_period = timedelta(days=1)
        
    elif loan.loan_product.repayment_frequency == 'weekly':
        interval_period = timedelta(days=7)
    else:
        interval_period = timedelta(days=30)
    
    return interval_period
#-- ends --

#get loan prevoius due date/start date
def get_previous_due_date(loan):
    previous_due_date = loan.due_date - get_interval_period(loan)
    return previous_due_date
#-- ends --
    
def installments(loanproduct):
    payment_frequency = loanproduct.repayment_frequency
    loan_term = loanproduct.loan_product_term
    term_period = loanproduct.loan_term_period

    if payment_frequency == 'onetime':
        return 1
    elif payment_frequency == 'daily':
        interval_duration = timedelta(days=1)
    elif payment_frequency == 'weekly':
        interval_duration = timedelta(days=7)
    else:
        interval_duration = timedelta(days=30)
    
    # Convert loan term to timedelta object
    if term_period == 'day':
        loan_term = timedelta(days=loan_term)
    elif term_period == 'week':
        loan_term = timedelta(weeks=loan_term)
    elif term_period == 'month':
        loan_term = timedelta(days=loan_term)*30 
    else:
        loan_term = timedelta(days=loan_term)*365

    # Calculate the number of payment intervals within the loan term
    num_intervals = loan_term // interval_duration

    # Round up to the nearest whole number of intervals
    num_installments = math.ceil(num_intervals)

    return num_installments
# -- ends 

#function to ge the total paybale of a loan
def total_interest(loan):
    rate_type = loan.loan_product.interest_type
    principal = loan.approved_amount or 0
    rate = loan.loan_product.interest_rate
    time = loan.loan_product.loan_product_term
    interest = 0
    
    if rate_type == 'flat rate':
        interest = int(principal) * time * rate / 100
    else:
        interest = (principal * time * rate) / (1 - (1 + rate)**(-time))

    return interest

def calculate_fined_amount(loan):
    start_date = loan.approved_date + timedelta(days=1)
    current_date = timezone.now()
    initial_fined_amount = (loan.approved_amount + total_interest(loan)) / installments(loan.loan_product)
    interval_period = get_interval_period(loan) #timedelta(days=50) format
    number_of_installments = installments(loan.loan_product)  

    #get difference between start date and current_date
    difference = (current_date - start_date).days
    #get expired payment intervals/installments
    expired_intervals = difference // interval_period.days
    if expired_intervals <= number_of_installments:
        fined_amount = initial_fined_amount * expired_intervals
    else:
        fined_amount = initial_fined_amount * number_of_installments
    return fined_amount
 
#function to get total penalitis 
def total_penalty(loan):
    current_date = timezone.now().date()
    penal_rate = loan.loan_product.penalty_value
    penalty_type = loan.loan_product.penalty_type
    fined_amount = calculate_fined_amount(loan)
    if loan.status in ['overdue','written off']:
        if loan.loan_product.penalty_frequency == 'onetime':
            period_overdue = 1
        elif loan.loan_product.penalty_frequency == 'daily':
            period_overdue = (current_date - loan.due_date.date()).days
        elif loan.loan_product.penalty_frequency == 'weekly':
            period_overdue = (current_date - loan.due_date.date()).days // 7
        else:
            #period_overdue = current_date - loan.due_date.date() # in months
            period_overdue = (current_date.year - loan.due_date.date().year) * 12 + (current_date.month - loan.due_date.date().month)
        if penalty_type == 'fixed_value':
            penalty_amount = loan.loan_product.penalty_value 
        else:
            penalty_amount = fined_amount * period_overdue * penal_rate / 100

        return penalty_amount

def total_payable_amount(loan):
    principal = loan.approved_amount or 0
    penalties = total_penalty(loan) or 0
    interest_amount = total_interest(loan)
    amount = penalties + interest_amount + principal
    return amount

#get due amount per install
def loan_due_amount(loan):
    payable = total_payable_amount(loan)
    installment = installments(loan)
    amount = payable / installment
    return amount

#initital due date upon loan approval
def loan_due_date(loan):  
    start_date = timezone.now() + timedelta(days=1)
     #because this function is called only when approving a loan.
    if loan.loan_product.repayment_frequency == 'onetime':
        # For one-time payments, the due date is simply the application date plus the loan product term
        if loan.loan_product.loan_term_period == 'day':
            return start_date + timedelta(days=loan.loan_product.loan_product_term)
        elif loan.loan_product.loan_term_period == 'week':
            return start_date + timedelta(days=loan.loan_product.loan_product_term * 7)
        elif loan.loan_product.loan_term_period == 'month':
            return start_date + timedelta(days=loan.loan_product.loan_product_term * 30)
        else:
            return start_date + timedelta(days=loan.loan_product.loan_product_term * 365)
    elif loan.loan_product.repayment_frequency == 'daily':
        return start_date + timedelta(days=1)
        
    elif loan.loan_product.repayment_frequency == 'weekly':
        return start_date + timedelta(days=7)
    else:
        return start_date + timedelta(days=30)   
# --ends  

#final payment date
def final_date(loan):
    start_date = loan.approved_date + timedelta(days=1) #grace period of one day
    loan_term = loan.loan_product.loan_product_term
    term_period = loan.loan_product.loan_term_period
    if term_period == 'day':
        loan_term = timedelta(days=loan_term)
    elif term_period == 'week':
        loan_term = timedelta(days=loan_term * 7)
    elif term_period == 'month':
        loan_term = timedelta(days=loan_term * 30)
    elif term_period == 'year':
        loan_term = timedelta(days=loan_term * 365)


    final_date = start_date + loan_term 
    return final_date
 
#calculate the service fee amount  
def get_service_fee(loan): 
    service_fee_type = loan.loan_product.service_fee_type 
    service_fee_value = loan.loan_product.service_fee_value
    approved_amount = int(loan.approved_amount)

    if approved_amount >= loan.loan_product.minimum_amount:
        if service_fee_type == 'fixed value':
            service_fee = service_fee_value
        elif service_fee_type == 'percentage':
            service_fee = approved_amount * service_fee_value * 0.01
        return service_fee

#function to fill due_amount field in Loan once loan is approved & final date
def save_due_amount(loan):
    payable = total_payable_amount(loan)
    installment = installments(loan.loan_product)
    amount = payable / installment
    loan.due_amount = amount
    loan.interest_amount = total_interest(loan)
    loan.service_fee_amount = get_service_fee(loan) 
    loan.final_due_date = final_date(loan) #fill final payment date 
    loan.save()

#update due amount if overdue
'''
The update_due_amount(loan) update loan due amount if a loan is overdue and attracts penalty.
Its called by a task on jekiiLMS/tasks/py 
Do not confuse it with update_due_amount(loan) function.
'''
def update_due_amount(loan):
    if loan.status == 'overdue':
        amount = loan.due_amount + total_penalty(loan)
        loan.due_amount = amount
        loan.save()
#-- ends --

#update member credit score
def update_credit_score(loan):
    credit_score = loan.member.credit_score
    if loan.status == 'overdue':
        credit_score -= 2
    elif loan.status == 'approved':
        credit_score += 1 
    elif loan.status == 'written off':
        credit_score = 0
    elif loan.status == 'rolled over':
        credit_score -= 3 
    elif loan.status == 'cleared':
        credit_score += 1   
    loan.member.previous_credit_score = loan.member.credit_score
    loan.member.credit_score = credit_score
    loan.member.save()
# -- ends 

