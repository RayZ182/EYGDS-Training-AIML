import pandas as pd

# Load processed visits CSV
df = pd.read_csv('processed_visits.csv')

# 1. Average cost per visit
avg_cost_per_visit = df['Cost'].mean()

# 2. Most visited doctor
# most_visited_doctor = df['DoctorID'].value_counts().idxmax()
most_visited_doctor = df['DoctorID'].value_counts().idxmax()

# 3. Number of visits per patient
visits_per_patient = df['PatientID'].value_counts()

# 4. Monthly revenue
monthly_revenue = df['Cost'].sum()

# Prepare KPI report dataframe
kpi_data = {
    'KPI': [
        'Average Cost Per Visit',
        'Most Visited Doctor',
        'Monthly Revenue'

    ],
    'Value': [
        avg_cost_per_visit,
        most_visited_doctor,
        monthly_revenue
    ]
}

kpi_df = pd.DataFrame(kpi_data)

# Save main KPI data to CSV
kpi_df.to_csv('kpi_report.csv', index=False, header = ['KPI', 'Value'])

visits_per_patient.to_csv('visits_per_patient.csv', header=['Number_of_Visits'])


print("KPI report saved as 'kpi_report.csv'.")
