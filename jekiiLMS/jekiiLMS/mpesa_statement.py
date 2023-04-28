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
