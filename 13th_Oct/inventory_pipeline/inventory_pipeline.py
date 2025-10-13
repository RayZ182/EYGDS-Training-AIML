import pandas as pd
from datetime import datetime

df = pd.read_csv('inventory.csv')

df['Restock Needed'] = df.apply(lambda x: "Yes" if x['Quantity'] < x['ReorderLevel'] else "No", axis = 1)
df['TotalValue'] = df['Quantity'] * df['PricePerUnit']

df.to_csv('restock_report.csv', index=False)
print(f"Inventory pipeline completed at {datetime.now()}")