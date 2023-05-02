from datetime import datetime
from loan.models import Collateral
from .credit_score import member_credit_score, update_credit_score



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
def get_amount_to_disburse(loan): 
    recommended_amount = calculate_loan_amount(loan)
    service_fee_type = loan.loan_product.service_fee_type
    service_fee_value = loan.loan_product.service_fee_value

    if recommended_amount > 0:
        if service_fee_type == 'fixed value':
            service_fee = recommended_amount - service_fee_value
        else:
            fee = recommended_amount * service_fee_value * 0.01
            service_fee = recommended_amount - fee
        return service_fee
    else:
        return 0

#clear loan
def clear_loan(loan):
    loan_balance = loan.loan_balance()
    today = datetime.today().strftime('%Y-%m-%d')
    if loan_balance <= 0 and loan.status == 'approved' or loan.status == 'overdue':
                loan.status = 'cleared'
                loan.cleared_date = today 
                loan.save()

#update member details after loan cleared               
def update_member_data(loan):
    if loan.status == 'cleared':
        member = loan.member
        member.previous_credit_score = member.credit_score
        #member.credit_score = member_credit_score(member)
        member.credit_score = update_credit_score(member)
        member.status = 'inactive'
        member.save() 

