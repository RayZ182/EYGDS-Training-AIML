import json
import logging

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    filename = 'app.log',
                    level = logging.DEBUG)

student = [
    {"name": "Rahul", "age": 21, "course": "AI", "marks": 85},
    {"name": "Priya", "age": 22, "course": "ML", "marks": 90}
]

# creating the json file
with open('students.json', 'w') as f:
    json.dump(student, f, indent = 4)
    logging.info('Student data created successfully!')

# reading the initial data
with open('students.json', 'r') as f:
    st = json.load(f)
    logging.info('Student data read successfully')

for stud in st:
    print(stud.get('name'))
logging.info('Student name printed successfully!')

# new student
new_stud = {
    "name" : "Arjun",
    "age" : 20,
    "course" : 'Data Science',
    "marks" : 78
}

# adding new Student
st.append(new_stud)
logging.info("New Student added!")

# adding new student to the json file
with open('students.json', 'w') as f:
    json.dump(st, f, indent = 4)
logging.info("Student data updated to students.json successfully!")
logging.info('File saved.')
