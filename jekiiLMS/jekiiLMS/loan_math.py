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