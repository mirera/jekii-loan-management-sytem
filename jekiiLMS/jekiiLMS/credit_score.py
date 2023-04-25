from datetime import timedelta
from django.utils import timezone

def member_credit_score(member):
    # Get the last cleared loan for the member
    last_loan = member.loans_as_member.filter(status='cleared').order_by('-cleared_date').first()
    # If the member has no cleared loans, return the default credit score
    if last_loan is None:
        return member.credit_score

    # Get the loan product associated with the last cleared loan
    loan_product = last_loan.loan_product

    # Calculate the time since the last cleared loan
    days_since_last_loan = (timezone.now() - last_loan.cleared_date).days

    # Calculate the expected interval between repayments based on loan product's repayment frequency
    if loan_product.repayment_frequency == 'onetime':
        expected_interval = loan_product.loan_term
    elif loan_product.repayment_frequency == 'daily':
        expected_interval = 1
    elif loan_product.repayment_frequency == 'weekly':
        expected_interval = 7
    elif loan_product.repayment_frequency == 'monthly':
        expected_interval = loan_product.loan_term
    else:
        expected_interval = 1

    # Calculate the expected number of intervals since the last cleared loan
    expected_intervals = days_since_last_loan // expected_interval

    # If the member paid on time, increase their credit score by 0.5 points per interval
    if expected_intervals > 0:
        member.credit_score += 0.5 * expected_intervals
    # If the member did not pay on time, deduct 0.5 points per interval late
    else:
        expected_intervals = abs(expected_intervals)
        member.credit_score -= 0.5 * expected_intervals

    # Make sure the credit score stays within the valid range of 0 to 100
    member.credit_score = max(0, min(100, member.credit_score))

    # Save the updated credit score to the database
    member.save()

    # Return the updated credit score
    return member.credit_score
