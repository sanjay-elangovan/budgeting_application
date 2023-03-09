import pandas as pd
import knowntransactions as known_fields
import json

with open('config.json', 'r') as f:
  config = json.load(f)
raw_datasources = config['datasource']

datasources = dict()
for source in raw_datasources:
    datasource = raw_datasources[source]
    datasources[source] = pd.read_csv(datasource['path'], skiprows=datasource['skiprows'])
    datasources[source].rename(columns=datasource["column_mapping"],inplace=True)

grouped_transactions = dict()
for datasource in datasources:
    transactions = datasources[datasource]

    typelist = []
    for row in transactions.iterrows():
        values = row[1]
        print("\nTransaction:")
        print(f"Date: {values['Date']}")
        print(f"Description: {values['Description']}")
        print(f"Amount: {values['Amount']}\n")
        print(config['categories'])      
        typelist.append(input("Transaction Type: "))

    if transactions['Amount'].dtypes == object:
        transactions['Amount'] = transactions['Amount'].str.replace(",","",regex=False)
        transactions['Amount'] = transactions['Amount'].str.replace("($","-",regex=False)
        transactions['Amount'] = transactions['Amount'].str.replace(")","",regex=False)
        transactions['Amount'] = transactions['Amount'].str.replace("$","",regex=False)
        transactions['Amount'] = transactions['Amount'].str.replace("+ ","", regex=False)
        transactions['Amount'] = transactions['Amount'].str.replace("- ","-", regex=False)
        transactions['Amount'] = transactions['Amount'].astype('float')
    
    transactions['Type'] = typelist
    grouped_transactions[datasource] = transactions[['Date','Description','Amount','Type']]

all_transactions = pd.DataFrame()
for i in grouped_transactions:
    all_transactions = pd.concat([all_transactions, grouped_transactions[i]],ignore_index=True)

all_transactions.to_csv('transactions_categorized.csv')

input("Reviewed transactions? ")

all_transactions = pd.read_csv('../transactions/cleaned_transactions/February/transactions_categorized.csv')
all_transactions.groupby('Type')['Amount'].sum().to_excel('aggregated_transactions.xlsx')    
