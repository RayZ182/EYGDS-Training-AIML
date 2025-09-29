use schoolDB;

create table teachers(
	teacher_id int auto_increment primary key,
	name varchar(50) not null,
    subject_id int,
    foreign key (subject_id) references subject(subject_id)
);

create table subject(
	subject_id int auto_increment primary key,
    subject_name varchar(50)
);

INSERT INTO Subject (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English

select * from teachers;
select * from subject;

-- inner join
select t.name, s.subject_name from
teachers t
inner join subject s
on t.subject_id = s.subject_id;

-- left join
select t.name, s.subject_name from
teachers t
left join subject s
on t.subject_id = s.subject_id;

-- right join
select t.name, s.subject_name from
teachers t
right join subject s
on t.subject_id = s.subject_id;

-- full join
select t.name, s.subject_name from
teachers t
left join subject s
on t.subject_id = s.subject_id

union

select t.name, s.subject_name from
teachers t
right join subject s
on t.subject_id = s.subject_id;