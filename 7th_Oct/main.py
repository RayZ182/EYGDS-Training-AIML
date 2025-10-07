from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for validation
class Student(BaseModel):
    id : int
    name : str
    age : int
    course : str

# In-memory database
students = [
    {"id" : 1, "name" : "Prince", "age" : 22, "course" : "RageBait"},
    {"id" : 2, "name" : "Mini Pekka", "age" : 20, "course" : "Pancakes"}
]

# GET Request
@app.get("/students")
def get_all_students():
    return {"student" : students }

# Another GET Request
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code= 404, detail= "Student not found")

# POST Request
@app.post("/students", status_code= 201)
def add_student(student: Student):
    students.append(student.dict())
    return {"message": "Student added successfully", "student" : student}

# PUT Request
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students[i] = updated_student.dict()
            return {"message": "Student Updated Successfully", "student": updated_student}
    raise HTTPException (status_code= 404, detail= "Student not found")

# DELETE Request
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students.pop(i)
            return {"message": "Student Deleted Successfully"}
    raise  HTTPException (status_code = 404, detail= "Student not found")