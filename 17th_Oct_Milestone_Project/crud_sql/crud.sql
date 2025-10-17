-- Create a database
create database healthdb;

-- Using the database
use healthdb;


-- Creating the tables
-- Patients
create table patients (
	PatientID varchar(50) primary key,
    Name varchar(50),
    Age int, 
    `Condition` varchar(50)
);

-- Doctors
create table doctors(
	DoctorID varchar(50) primary key,
    Name varchar(50),
    Specialization varchar(50)
);

# Insert Data

insert into patients (PatientID, Name, Age, `Condition`) values
	('P001','Neha',32,'Fever'),
    ('P002','Arjun',45,'Diabetes'),
    ('P003','Sophia',28,'Hypertension'),
    ('P004','Ravi',52,'Asthma'),
    ('P005','Meena',38,'Arthritis');
    
insert into doctors (DoctorID, Name, Specialization) values
	('D101','Dr. Patel','General Physician'),
    ('D102','Dr. Khan','Endocrinologist'),
    ('D103','Dr. Verma','Cardiologist'),
    ('D104','Dr. Rao','Pulmonologist');

-- READ 
select * from patients;
select * from doctors;

select * from patients where age > 40;

-- ADD
insert into patients (PatientID, Name, Age, `Condition`) values
	('P005', 'Mohan Kumar', 56, 'Cancer');
    
-- UPDATE

update patients set `Condition` = 'Common Cold'
	where PatientID = 'P003';
    
update doctors set Name = 'Dr. Mitra'
	where DoctorID = 'D103';
    
-- DELETE
delete from patients where PatientID = 'P001';
delete from doctors where DoctorID = 'D104';