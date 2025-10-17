import pandas as pd

# Load processed visits CSV (assuming it has all necessary info like DoctorID, PatientID, Cost, Date)
df = pd.read_csv('processed_visits.csv')

# 1. Average cost per visit (simple mean)
avg_cost_per_visit = df['Cost'].mean()

# 2. Most visited doctor (DoctorID with highest number of visits)
most_visited_doctor = df['DoctorID'].value_counts().idxmax()
most_visited_doctor_visits = df['DoctorID'].value_counts().max()

# 3. Number of visits per patient (PatientID counts)
visits_per_patient = df.groupby('PatientID')['VisitID'].count()

# 4. Monthly revenue (sum of Cost grouped by Month)
monthly_revenue = df.groupby('Month')['Cost'].sum()

# Prepare KPI report dataframe
kpi_data = {
    'KPI': [
        'Average Cost Per Visit',
        'Most Visited Doctor',
        'Most Visited Doctor Visits',
        'Monthly Revenue'

    ],
    'Value': [
        avg_cost_per_visit,
        most_visited_doctor,
        most_visited_doctor_visits,
        monthly_revenue
    ]
}

kpi_df = pd.DataFrame(kpi_data)

# Save main KPI data to CSV
kpi_df.to_csv('kpi_report.csv', index=False)

# Save visits per patient and monthly revenue to separate sheets in Excel or separate CSVs
visits_per_patient.to_csv('visits_per_patient.csv', header=['Number_of_Visits'])


print("KPI report saved as 'kpi_report.csv'.")
