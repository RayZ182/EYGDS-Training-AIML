import pandas as pd
import numpy as np

data = {
    "name" : ["Riju", "Sayan", "Ritankar"],
    "age" : [21, 22, 23],
    "course" : ['python', 'dsa', 'AI'],
    "marks" : [77,89,90]
}

df = pd.DataFrame(data)

#Add Pass/Fail
df["result"] = np.where(df["marks"] >= 80, "Pass", "Fail")

#Update marks
df.loc[df["name"] == "Riju", "marks"] = 90

print(df)