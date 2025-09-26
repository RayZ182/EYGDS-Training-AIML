use schooldb;

create table employee (
id int auto_increment primary key,
name varchar(50) not null,
age int,
department varchar(50) not null, 
salary decimal(10,2)
);

insert into employee (name, age, department, salary) values
	('Riju', 22, 'AI & DATA', 35000),
    ('Rishi', 22, 'Banking', 45000),
    ('Priya', 22, 'Java', 30000),
    ('Subhro', 22, 'Oracle', 50000),
    ('Mega Knight', 67, 'Bming', 7);
    
select * from employee;


update employee set name = 'Hog Rider', age = 25, department = 'Defence', salary = 4
where id = 4;

delete from employee where id = 3;