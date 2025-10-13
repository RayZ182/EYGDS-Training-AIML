import pandas as pd

# Extract the data
df = pd.read_csv('students.csv')

# Transform the data (Data Pre-Processing)

# Removing null values
df.dropna(inplace=True)

# Correcting Data Type
df['Marks'] = df['Marks'].astype(int)

# creating a new column
df['Result'] = df['Marks'].apply(lambda x: "Pass" if x >=60 else "Fail")

# Loading into a new csv
df.to_csv('cleaned_students.csv', index = False)
print("ETL Process is done!")