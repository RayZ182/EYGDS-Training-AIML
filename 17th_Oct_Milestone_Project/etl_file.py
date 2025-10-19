import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = 'app.log',
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def process_visits(visits_csv, patients_csv, doctors_csv):
    try:
        patients = pd.read_csv(patients_csv)
        logging.info("Patients file processed successfully.")
    except FileNotFoundError:
        logging.error("patients.csv file not found.")

    try:
        doctors = pd.read_csv(doctors_csv)
        logging.info("Doctors file processed successfully.")
    except FileNotFoundError:
        logging.error("doctors.csv file not found.")

    try:
        visits_df = pd.read_csv(visits_csv)
        logging.info("Visit file processed successfully.")
    except FileNotFoundError:
        logging.error("visits.csv file not found.")

    if doctors["DoctorID"].isnull().any():
        logging.error("Doctor ID doesn't exist.")
        raise ValueError("Doctor ID missing")

    # Join visits with patients on PatientID == id (assuming patients.id == PatientID)
    df = visits_df.merge(patients, on='PatientID', how='left')

    # Join the above result with doctors on DoctorID
    df = df.merge(doctors, on='DoctorID', how='left')

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Add 'Month' column
    df['Month'] = df['Date'].dt.month_name()

    # Calculate FollowUpRequired:
    visit_counts = df.groupby('PatientID')['VisitID'].transform('count')
    df['FollowUpRequired'] = visit_counts > 1

    # Save to CSV

    df.to_csv('processed_visits.csv', index=False)

    print("Processed visits saved to 'processed_visits.csv'")
    logging.info(f"Processed visits saved to process_visits.csv")

if __name__ == "__main__":
    process_visits('visits.csv', 'patients.csv', 'doctors.csv')