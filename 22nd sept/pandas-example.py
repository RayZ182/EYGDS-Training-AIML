import pandas as pd
import numpy as np

data = {
    "name" : ["Riju", "Sayan", "Ritankar"],
    "age" : [21, 22, 23],
    "course" : ['python', 'dsa', 'AI'],
    "marks" : [77,89,90]
}

df = pd.DataFrame(data)
# print(df["name"])
# print(df[["name","marks"]])
# print(df.iloc[2])
# print(df.loc[2, "name"])
# print(df)

# Filter the data
high_scorers = df[df["marks"]>85]
print(high_scorers)
