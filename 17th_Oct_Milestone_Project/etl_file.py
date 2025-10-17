import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = 'app.log',
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def process_visits(visits_df, patients_csv='patients.csv', doctors_csv='doctors.csv', output_csv='processed_visits.csv'):
    try:
        patients = pd.read_csv(patients_csv)
        logging.info("Patients file processed successfully.")
    except FileNotFoundError:
        logging.error("patients.csv file not found.")
        raise

    try:
        doctors = pd.read_csv(doctors_csv)
        logging.info("Doctors file processed successfully.")
    except FileNotFoundError:
        logging.error("doctors.csv file not found.")
        raise

    if doctors["DoctorID"].isnull().any():
        logging.error("Doctor ID doesn't exist.")
        raise ValueError("Doctor ID missing required value")

    # Join visits with patients on PatientID == id (assuming patients.id == PatientID)
    df = visits_df.merge(patients, on='PatientID', how='left')

    # Join the above result with doctors on DoctorID
    df = df.merge(doctors, on='DoctorID', how='left')

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Add 'Month' column
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    # Calculate FollowUpRequired:
    visit_counts = df.groupby('PatientID')['VisitID'].transform('count')
    df['FollowUpRequired'] = visit_counts > 1

    # Save to CSV

    df.to_csv('processed_visits.csv', index=False)

    print("Processed visits saved to 'processed_visits.csv'")
    logging.info(f"Processed visits saved to process_visits.csv")