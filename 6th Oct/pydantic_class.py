from pydantic import BaseModel

# define a model (schema)

class Student(BaseModel):
    name : str
    age : int
    email : str

# valid data
data = {"name" : "priya", "age" : 22, "email" : "priya@g.com"}

student = Student(**data)
print(student.age)