

#calculate the amount to approve 
def get_approved_amount(loan): 
    pass

#checking if collateral is sufficient
def is_sufficient_collateral(loan):
    recommended_amount = get_approved_amount(loan)
    required_collateral_value = recommended_amount * 3
    total_estimated_value = 0
    
    # Loop through all collaterals of the loan object
    collaterals = loan.collateral_set.all()
    for collateral in collaterals:
        total_estimated_value += collateral.estimated_value

    return total_estimated_value >= required_collateral_value

#calculate the amount to disburse 
def get_amount_to_disburse(loan): 
    recommended_amount = get_approved_amount(loan)
    service_fee_type = loan.loan_product.service_fee_type
    service_fee_value = loan.loan_product.service_fee_value

    if service_fee_type == 'fixed value':
        service_fee = recommended_amount - service_fee_value
    else:
        fee = service_fee_value * 1/100
        service_fee = recommended_amount - fee
    return service_fee

