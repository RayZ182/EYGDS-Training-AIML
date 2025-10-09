from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)

#Pydantic Model
class Student(BaseModel):
    id : int
    name : str
    stream : str
    cgpa : float

# in memory database
students = [
    {"id": 1, "name": "sOm", "stream": "IOT", "cgpa": 8.67},
    {"id": 2, "name": "Austin", "stream": "CSE", "cgpa": 8.92},
    {"id": 3, "name": "Adam", "stream": "AIML", "cgpa": 9.02},
    {"id": 4, "name": "Brawk", "stream": "ECE", "cgpa": 6.7},
    {"id": 5, "name": "Ethan", "stream": "MBA", "cgpa": 9.7}
]

# GET all request
@app.get("/students")
def get_all():
    return students
