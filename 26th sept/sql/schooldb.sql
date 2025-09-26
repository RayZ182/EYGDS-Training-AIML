-- create a database
CREATE database SchoolDB;

-- use this database
USE SchoolDB;

-- create a table
create table students(
	id int auto_increment primary key,
    name varchar(50),
    age int,
    course varchar(50),
    marks int
);

-- inserting rows
insert into students (name, age, course, marks) values
	('Riju', 22, 'OOPs', 89),
    ('Rishi', 22, 'Finance', 90),
    ('Priya', 36, 'SpringBoot', 77),
    ('Subhro', 50, 'CyberSecurity', 99);
    
-- show the table
select * from students;
-- this is CRUD Operation (Create, Read, Update, Delete)

-- select specific columns
select names, course from students;

select name, course from students where marks >80;

-- updating rows
update students set course = 'AI';

update students set course = 'Advanced AI', marks = 95 where id = 4;

-- delete
delete from students where id = 3;