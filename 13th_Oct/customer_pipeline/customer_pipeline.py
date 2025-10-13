import pandas as pd
from datetime import datetime

df = pd.read_csv('customers.csv')

df['Age Group'] = df['Age'].apply(lambda x: "Young" if x < 30 else "Adult" if x < 50 else "Senior")

# filter customer below 20
df = df[df["Age"] >= 20]

df.to_csv('filtered_customer.csv', index=False)
print(f"Pipeline Completed as {datetime.now()}")