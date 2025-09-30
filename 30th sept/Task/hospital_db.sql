create database hospitalDB;
use hospitalDB;

create table patients(
	patient_id INT PRIMARY KEY,
	name VARCHAR(50),
	age INT,
	gender CHAR(1),
	city VARCHAR(50)
);

create table doctors(
	doctor_id INT PRIMARY KEY,
	name VARCHAR(50),
	specialization VARCHAR(50),
	experience INT
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

create table medicalRecords(
	record_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis VARCHAR(100),
    treatment VARCHAR(100),
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

create table billing(
	bill_id INT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    bill_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- INSERTION
-- patient
insert into patients values
(1, 'Taranath', 57, 'M', 'Kolkata'),
(2, 'Greg', 15, 'M', 'Mumbai'),
(3, 'Susan', 45, 'F', 'Mumbai'),
(4, 'Frank', 50, 'M', 'Tumling'),
(5, 'Rodrick', 22, 'M', 'Delhi'),
(6, 'Manny', 3, 'M', 'Pune'),
(7, 'Rowley', 15, 'M', 'Gangtok'),
(8, 'Chirag', 13, 'M', 'Kochi'),
(9, 'Fregly', 15, 'M', 'Bangalore'),
(10, 'Sweaty', 4, 'M', 'Darjeeling');

-- doctors
insert into doctors values
(1, 'Mega Knight', 'Cardiology', 7),
(2, 'Night Witch', 'Cardiology', 5),
(3, 'Archer', 'Orthopedics', 9),
(4, 'Goblin Machine', 'Pediatrics', 2),
(5, 'Boss Bandit', 'Neurology', 1);

-- appointments
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, status)
VALUES
(1, 1, 1, '2025-09-01', 'Completed'),
(2, 2, 2, '2025-09-03', 'Scheduled'),
(3, 3, 3, '2025-09-05', 'Completed'),
(4, 4, 4, '2025-09-07', 'Cancelled'),
(5, 5, 5, '2025-09-10', 'Completed'),
(6, 6, 1, '2025-09-12', 'Scheduled'),
(7, 7, 2, '2025-09-14', 'Completed'),
(8, 8, 3, '2025-09-16', 'Scheduled'),
(9, 9, 4, '2025-09-18', 'Completed'),
(10, 10, 5, '2025-09-20', 'Scheduled');

-- medical records
INSERT INTO medicalRecords (record_id, patient_id, doctor_id, diagnosis, treatment, date)
VALUES
(1, 1, 1, 'Hypertension', 'Medication A', '2025-09-01'),
(2, 2, 2, 'Fracture', 'Cast & Rest', '2025-09-03'),
(3, 3, 3, 'Flu', 'Antivirals', '2025-09-05'),
(4, 4, 4, 'Eczema', 'Topical Cream', '2025-09-07'),
(5, 5, 5, 'Migraine', 'Painkillers', '2025-09-10'),
(6, 6, 1, 'High Cholesterol', 'Diet & Medication', '2025-09-12'),
(7, 7, 2, 'Arthritis', 'Physiotherapy', '2025-09-14'),
(8, 8, 3, 'Allergy', 'Antihistamines', '2025-09-16'),
(9, 9, 4, 'Acne', 'Skin Treatment', '2025-09-18'),
(10, 10, 5, 'Epilepsy', 'Anti-seizure meds', '2025-09-20');

-- billing
INSERT INTO billing (bill_id, patient_id, amount, bill_date, status)
VALUES
(1, 1, 1500.00, '2025-09-01', 'Paid'),
(2, 2, 2000.00, '2025-09-03', 'Unpaid'),
(3, 3, 800.00, '2025-09-05', 'Paid'),
(4, 4, 1200.00, '2025-09-07', 'Unpaid'),
(5, 5, 2500.00, '2025-09-10', 'Paid'),
(6, 6, 1800.00, '2025-09-12', 'Unpaid'),
(7, 7, 2200.00, '2025-09-14', 'Paid'),
(8, 8, 950.00, '2025-09-16', 'Unpaid'),
(9, 9, 1100.00, '2025-09-18', 'Paid'),
(10, 10, 3000.00, '2025-09-20', 'Unpaid');

-- basic queries
-- List all patients assigned to a cardiologist.
select pt.name as patient, d.name as doctor
from appointments ap
join patients pt on ap.patient_id = pt.patient_id
join doctors d on ap.doctor_id = d.doctor_id
where d.specialization = 'Cardiology';

-- Find all appointments for a given doctor.
select d.name, ap.appointment_date
from appointments ap
join doctors d on ap.doctor_id = d.doctor_id
group by d.name, ap.appointment_date;

-- Show unpaid bills of patients.
select bill_id, bill_date, amount, status
from billing
where status = 'Unpaid';

-- stored procedure
-- Procedure: GetPatientHistory(patient_id) → returns all visits, diagnoses, and treatments for a patient.

delimiter $$
create procedure GetPatientHistory(in PTID varchar(10))
begin
	select pt.name, med.diagnosis, med.treatment, med.date
    from medicalRecords med
    join patients pt on med.patient_id = pt.patient_id
    where pt.patient_id = PTID;
end$$

delimiter ;
call GetPatientHistory(2);

-- Procedure: GetDoctorAppointments(doctor_id) → returns all appointments for a doctor.
delimiter $$
create procedure GetDoctorAppointments(in DID int)
begin
	select d.name, ap.appointment_date
    from appointments ap
    join doctors d on ap.doctor_id = d.doctor_id
    where d.doctor_id = DID;
end$$

delimiter ;
call GetDoctorAppointments(3);

drop procedure if exists GetDoctorAppointments;