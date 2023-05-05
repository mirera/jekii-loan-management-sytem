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
    print(pdf)
    page = pdf[0]
    print(page)
    
    table = []
    for i in range(page.number):
        table = page.extract_table(table_settings={"horizontal_strategy": "lines", "explicit_vertical_lines": []})
        for row in table:
            row_data = [cell.strip() for cell in row]
            table.append(row_data)
    print('below is the table')
    print(table)
    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(table, columns=['Receipt No.', 'Completion Time', 'Details', 'Transaction Status', 'Paid In', 'Withdrawn', 'Balance'])
    print('Below is the df')
    print(df)
    # Filter the columns of interest
    df = df[['Completion Time', 'Details', 'Paid In', 'Withdrawn']]

    # Convert the 'Paid In' and 'Withdrawn' columns to numeric data type
    df['Paid In'] = pd.to_numeric(df['Paid In'])
    df['Withdrawn'] = pd.to_numeric(df['Withdrawn'])

    return df # return the dataframe with columns Paid in and Withdrwarn having integer type or numeric

#get loan table for each available creditor
def creditors_table(df):
    # Filter the DataFrame based on the creditor names in the 'Details' column
    creditor_tables = {}
    for creditor in known_creditors:
        creditor_table = df[df['Details'].str.contains(creditor)]
        if not creditor_table.empty:
            creditor_tables[creditor] = creditor_table
    return creditor_tables # a dictionary of creditor and their loan df

#To get the number of loans the borrower received from each creditor 
def total_loans_received(creditor_tables):
    # Get the number of loans for each creditor
    for creditor, table in creditor_tables.items():
        num_loans = table['Paid In'].nunique()
        print(f'{creditor} has given {num_loans} loans to the borrower.')
    return num_loans

def total_active_loans(creditor_tables):
    # Iterate through each creditor's table and calculate number of active loans
    for creditor, table in creditor_tables.items():
        num_active_loans = 0
        cumulative_withdrawn = 0
        
        for i, row in table.iterrows():
            if row['Paid In'] > cumulative_withdrawn:
                num_active_loans += 1
                
            cumulative_withdrawn += row['Withdrawn']
            
        print(f'Number of active loans for {creditor}: {num_active_loans}')
    return num_active_loans

#total loan balances from all creditors
def total_loan_blncs(creditor_tables):
    pass

#amount loaned by each creditor for each occassion
def principal_amounts(creditor_tables):
    dict_of_amounts = []
    return dict_of_amounts


#calculate recommened amount based on mpesa statmet
def amount_based_mp(loan):
    #find average of averages of all the principal amount a creditor a lended the borrower
    amount = 2
    return amount

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

def _loans_table(file_path, file_password):

    # Open the PDF file with password
    pdf = fitz.open(file_path)
    pdf.authenticate(password=file_password)

    # Get the first page
    print(pdf)
    page = pdf[0]
    print(page)

    # Extract the table data
    table = []
    for i in range(page.number):
        table = page.extract_table(table_settings={"horizontal_strategy": "lines", "explicit_vertical_lines": []})
        for row in table:
            row_data = [cell.strip() for cell in row]
            table.append(row_data)
    print('below is the table')
    print(table)
    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(table, columns=['Receipt No.', 'Completion Time', 'Details', 'Transaction Status', 'Paid In', 'Withdrawn', 'Balance'])
    print('Below is the df')
    print(df)
    # Filter the columns of interest
    df = df[['Completion Time', 'Details', 'Paid In', 'Withdrawn']]

    # Convert the 'Paid In' and 'Withdrawn' columns to numeric data type
    df['Paid In'] = pd.to_numeric(df['Paid In'])
    df['Withdrawn'] = pd.to_numeric(df['Withdrawn'])

    return df # return the dataframe with columns Paid in and Withdrwarn having integer type or numeric