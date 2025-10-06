class Student:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

data = {"name" : "priya", "age" : "twenty two", "email" : "priya@g.com"}
student = Student(**data)
print(student.age)