from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import logging

# configure logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = 'app.log',
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Pydantic Class
class Patient(BaseModel):
    PatientID: str
    Name: str
    Age: int
    Condition: str

class Doctor(BaseModel):
    DoctorID: str
    Name: str
    Specialization: str

# Loading  patients.csv and convert to list of dicts
df_patients = pd.read_csv("patients.csv")
patients = df_patients.to_dict(orient="records")

# Load doctors.csv and convert to list of dicts
df_doctors = pd.read_csv("doctors.csv")
doctors = df_doctors.to_dict(orient="records")


# Patient Routes

# Get all patients data
@app.get("/patients")
def get_all_patients():
    logging.info("All Patients Displayed")
    return {"patients": patients}

# Add a new patient
@app.post("/patients", status_code=201)
def add_patient(new_pat: Patient):
    for pat in patients:
        if pat["PatientID"] == new_pat.PatientID:
            logging.error(f"PatientID {new_pat.PatientID} Already exists")
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    patients.append(new_pat.dict())
    logging.info(f"New Patient Added : {new_pat.PatientID}")
    return {"message": "Patient added successfully", "patient": new_pat}

# Update an existing Patient record
@app.put("/patients/{pid}")
def update_patients(pid: str, updated_pat: Patient):
    if pid != updated_pat.PatientID:
        logging.error("Mismatch in PatientID")
        raise HTTPException(status_code=400, detail="ID in path and body do not match")
    for i, pat in enumerate(patients):
        if pat["PatientID"] == pid:
            patients[i] = updated_pat.dict()
            logging.info(f"Patient ID {pid} updated successfully")
            return {"message": "Patient updated successfully", "patient": updated_pat}
    logging.error(f"Patient ID {pid} does not exist")
    raise HTTPException(status_code=404, detail="Patient not found")

# Delete a Patient record
@app.delete("/patients/{pid}", status_code=200)
def delete_patient(pid: str):
    for pat in patients:
        if pat["PatientID"] == pid:
            patients.remove(pat)
            logging.info(f"Patient ID {pid} deleted successfully")
            return {"message": "Patient deleted successfully", "patient": pat}
    raise HTTPException(status_code=404, detail="Patient not found")


# Doctor Routes

# Get all doctor names
@app.get("/doctors")
def get_all_doctors():
    logging.info("All Doctors Displayed")
    return {"doctors": doctors}

# Add a new Doctor Record
@app.post("/doctors", status_code=201)
def add_doctor(new_doc: Doctor):
    for doc in doctors:
        if doc["DoctorID"] == new_doc.DoctorID:
            logging.error(f"DoctorID {new_doc.DoctorID} Already exists")
            raise HTTPException(status_code=400, detail="Doctor with this ID already exists")

    doctors.append(new_doc.dict())
    logging.info(f"New Doctor Added : {new_doc.DoctorID}")
    return {"message": "Doctor added successfully", "doctor": new_doc}

# Update an existing Doctor
@app.put("/doctors/{doc_id}")
def update_doctor(doc_id: str, updated_doc: Doctor):
    if doc_id != updated_doc.DoctorID:
        logging.error("Mismatch in DoctorID")
        raise HTTPException(status_code=400, detail="ID in path and body do not match")
    for i, doc in enumerate(doctors):
        if doc["DoctorID"] == doc_id:
            doctors[i] = updated_doc.dict()
            logging.info(f"Doctor ID {doc_id} updated successfully")
            return {"message": "Doctor updated successfully", "doctor": updated_doc}
    logging.error(f"Doctor ID {doc_id} does not exist")
    raise HTTPException(status_code=404, detail="Doctor not found")


@app.delete("/doctors/{doc_id}", status_code=200)
def delete_doctor(doc_id: str):
    for doc in doctors:
        if doc["DoctorID"] == doc_id:
            doctors.remove(doc)
            logging.info(f"Doctor ID {doc_id} deleted successfully")
            return {"message": "Doctor deleted successfully", "doctor": doc}
    logging.error(f"Doctor ID {doc_id} does not exist")
    raise HTTPException(status_code=404, detail="Doctor not found")

