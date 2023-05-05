from datetime import timedelta, datetime, date, time
from dateutil.relativedelta import relativedelta
import math
import pytz

#function to ge the total paybale of a loan
def total_interest(loan):
    rate_type = loan.loan_product.interest_type
    principal = loan.approved_amount or 0
    rate = loan.loan_product.interest_rate
    time = loan.loan_product.loan_product_term
    interest = 0

    if rate_type == 'flat rate':
        interest = principal * time * rate / 100
    else:
        interest = principal * time * rate
        (rate * principal) / (1 - (1 + rate)**(-time))

    return interest

#function to get total penalitis 
def total_penalty(loan):
    principal = loan.approved_amount
    rate_or_value = loan.loan_product.penalty_value
    penalty_type = loan.loan_product.penalty_type
    penalty = 0
    if loan.status == 'overdue':
        if penalty_type == 'fixed_value':
                penalty = rate_or_value
        elif penalty_type == 'percentage of principal':
                penalty = (principal * rate_or_value) / 100
        elif penalty_type == 'percentage of principal interest':
                penalty = (principal + total_interest(loan) ) * rate_or_value / 100 
    else:
        penalty = 0
    return penalty

def total_payable_amount(loan):
    principal = loan.approved_amount or 0
    penalties = total_penalty(loan)
    interest_amount = total_interest(loan)
    amount = penalties + interest_amount + principal
    return amount

#get the number of installment
def num_installments(loan):
    payment_frequency = loan.loan_product.repayment_frequency
    loan_term = loan.loan_product.loan_product_term
    term_period = loan.loan_product.loan_term_period

    if payment_frequency == 'onetime':
        return 1
    elif payment_frequency == 'daily':
        interval_duration = timedelta(days=1)
    elif payment_frequency == 'weekly':
        interval_duration = timedelta(weeks=1)
    else:
        interval_duration = relativedelta(months=1)
    
    # Convert loan term to timedelta object
    if term_period == 'day':
        loan_term = timedelta(days=loan_term)
    elif term_period == 'week':
        loan_term = timedelta(weeks=loan_term)
    elif term_period == 'month':
        loan_term = relativedelta(months=loan_term)
    else:
        loan_term = relativedelta(years=loan_term)

    # Calculate the number of payment intervals within the loan term
    num_intervals = loan_term / interval_duration

    # Round up to the nearest whole number of intervals
    num_installments = math.ceil(num_intervals)

    return num_installments
#get due amount per install
def loan_due_amount(loan):
    payable = total_payable_amount(loan)
    installments = num_installments(loan)
    amount = payable / installments
    return amount

def loan_due_date(loan):
    #change today datetime to today midnight
    tz = pytz.timezone('UTC')
    today_date = date.today()
    midnight = time.min
    today = datetime.combine(today_date, midnight, tz)
     #because this function is called only when approving a loan.
    if loan.loan_product.repayment_frequency == 'onetime':
        # For one-time payments, the due date is simply the application date plus the loan product term
        if loan.loan_product.loan_term_period == 'day':
            return today + timedelta(days=loan.loan_product.loan_product_term)
        elif loan.loan_product.loan_term_period == 'week':
            return today + timedelta(weeks=loan.loan_product.loan_product_term)
        elif loan.loan_product.loan_term_period == 'month':
            return today + relativedelta(months=loan.loan_product.loan_product_term)
        else:
            return today + relativedelta(years=loan.loan_product.loan_product_term)
    elif loan.loan_product.repayment_frequency == 'daily':
        return today + timedelta(days=1)
        
    elif loan.loan_product.repayment_frequency == 'weekly':
        return today + timedelta(weeks=1)
    else:
        return today + timedelta(months=1)    