import fitz
import pandas as pd



#prepare list of all creditors 
known_creditors = ['KISMAT', 'FOURTH GENERATION CAPITAL', 'YEHU', 'MULLA PRIDE LIMITED',
                     'YESCASH', 'AZURA CREDIT LIMITED', 'LINK CASH', 'SURE CRED CAPITAL LIMITED', 
                     'CLOUDLOAN', 'ZENKA DIGITAL LIMITED'
                     ]


def get_loans_table(file_path, file_password):

    # Open the PDF file with password
    pdf = fitz.open(file_path)
    pdf.authenticate(password=file_password)

    # Get the first page
    page = pdf[0]

    # Extract the table data
    table = []
    for i in range(page.number):
        table = page.extract_table(table_settings={"horizontal_strategy": "lines", "explicit_vertical_lines": []})
        for row in table:
            row_data = [cell.strip() for cell in row]
            table.append(row_data)

    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(table, columns=['Receipt No.', 'Completion Time', 'Details', 'Transaction Status', 'Paid In', 'Withdrawn', 'Balance'])

    # Filter the columns of interest
    df = df[['Completion Time', 'Details', 'Paid In', 'Withdrawn']]

    # Convert the 'Paid In' and 'Withdrawn' columns to numeric data type
    df['Paid In'] = pd.to_numeric(df['Paid In'])
    df['Withdrawn'] = pd.to_numeric(df['Withdrawn'])

    return df # return the dataframe with columns Paid in and Withdrwarn having integer type or numeric


#calculating loan amount based on credit score
def amount_based_cs(loan):
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
    
    return amount_to_approve

#calculating loan amount to disbursw
def final_recommended_amount(loan):
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