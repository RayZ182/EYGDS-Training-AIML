create database CompanyDB;

use CompanyDb;

-- Department Table
create table Department (
	dept_id int auto_increment primary key,
    dept_name varchar(50) not null
);

-- Employee Table
create table employee (
	emp_id int auto_increment primary key,
    name varchar(50),
    age int,
    salary decimal(10,2),
    dept_id int,
    foreign key (dept_id) references Department(dept_id)
)

-- Inserting into Departments
insert into department (dept_name) values
	('IT'),
    ('HR'),
    ('Finance'),
    ('Sales');
    
select * from department;
    
INSERT INTO employee (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, 3),   -- Finance
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales

select * from employee;

ALTER TABLE employee DROP FOREIGN KEY employee_ibfk_1;

TRUNCATE TABLE employee;
TRUNCATE TABLE department;

INSERT INTO department (dept_name) VALUES
('IT'),         -- id = 1
('HR'),         -- id = 2
('Finance'),    -- id = 3
('Sales'),      -- id = 4
('Marketing');  -- id = 5 

INSERT INTO Employee (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, NULL),-- 
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales

-- inner join
select e.name, e.salary, d.dept_name from
employee e
inner join department d
on e.dept_id = d.dept_id;

-- left join
select e.name, e.salary, d.dept_name from
employee e
left join department d
on e.dept_id = d.dept_id;

-- right join
select e.name, e.salary, d.dept_name from
employee e
right join department d
on e.dept_id = d.dept_id;

-- full join
select e.name, e.salary, d.dept_name from
employee e
left join department d
on e.dept_id = d.dept_id

union

select e.name, e.salary, d.dept_name from
employee e
right join department d
on e.dept_id = d.dept_id;