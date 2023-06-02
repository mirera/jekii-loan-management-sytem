from datetime import datetime
from django.utils import timezone
from django.db.models import Sum


def member_credit_score(member):
    credit_score = member.credit_score
    # Get the current member active loan
    active_loan = member.loans_as_member.filter(status=('approved', 'overdue')).order_by('-approved_date').first()
    
    #current_date = datetime.now().date()
    current_date = timezone.now()

    # If the member has no cleared loans, return the default credit score
    if active_loan is None:
        return credit_score
    
    # Get the last repayment made by the member
    last_repayment = active_loan.repayments.filter(date_paid__lte=active_loan.next_payment_date()).order_by('-date_paid').first()

    #get the due date of the active loan
    next_payment_date = active_loan.next_payment_date()
    previous_payment_date = active_loan.previous_payment_date()
    due_date = next_payment_date if current_date <= next_payment_date else previous_payment_date

    
    # Get the amount due and due date for the last repayment made by the member
    amount_due_per_interval = active_loan.amount_due_per_interval()
    repayment_frequency = active_loan.loan_product.repayment_frequency
    previous_payment_date = active_loan.previous_payment_date()

    # Get the total amount of loan repayments made
    if active_loan.approved_date <= due_date:
        total_repayments = active_loan.repayments.filter(date_paid__lte=due_date).aggregate(Sum('amount'))['amount__sum']
    else:
        total_repayments = active_loan.repayments.filter(date_paid__gt=previous_payment_date, date_paid__lte=due_date).aggregate(Sum('amount'))['amount__sum']

    if last_repayment is None and current_date > due_date :
        loan_product_term = active_loan.loan_product.loan_product_term
        # deduct the credit score change based on the repayment frequency
        if repayment_frequency == 'onetime' or repayment_frequency == 'monthly':
            credit_score -= 1
        elif repayment_frequency == 'weekly':
            credit_score -= 0.5
        elif repayment_frequency == 'daily':
            if active_loan.loan_product.loan_term_period == 'day':
                loan_product_term = loan_product_term * 1 
            elif active_loan.loan_product.loan_term_period == 'week':
                loan_product_term = loan_product_term * 7 #change loan term to days
            elif active_loan.loan_product.loan_term_period == 'month':
                loan_product_term = loan_product_term * 30
            elif active_loan.loan_product.loan_term_period == 'year':
                loan_product_term = loan_product_term * 365
                credit_score -= 4 / loan_product_term
    else:
        if repayment_frequency == 'onetime' or repayment_frequency == 'monthly':
            if total_repayments >= amount_due_per_interval and last_repayment.date_paid <= due_date:
                # add the credit score 
                if repayment_frequency == 'onetime' or repayment_frequency == 'monthly':
                    credit_score += 1
                elif repayment_frequency == 'weekly':
                    credit_score += 0.5
                elif repayment_frequency == 'daily':
                    if active_loan.loan_product.loan_term_period == 'day':
                        loan_product_term = loan_product_term * 1 
                    elif active_loan.loan_product.loan_term_period == 'week':
                        loan_product_term = loan_product_term * 7 #change loan term to days
                    elif active_loan.loan_product.loan_term_period == 'month':
                        loan_product_term = loan_product_term * 30
                    elif active_loan.loan_product.loan_term_period == 'year':
                        loan_product_term = loan_product_term * 365
                        credit_score += 4 / loan_product_term
    # Make sure the credit score stays within the valid range of 0 to 100
    credit_score = max(0, min(100,credit_score))
    member.save()
    return credit_score

def update_credit_score(member):
    credit_score = member.credit_score
    credit_score += 2
    return credit_score