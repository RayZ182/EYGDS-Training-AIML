from fastapi import FastAPI

# create fastapi instance
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message" : "welcome to FastAPI Demo"}

# path parameter example
@app.get("/students/{student_id}")
def get_student(student_id : int):
    return {"student_id" : student_id, "name" : "Rahul", "subject" : "AI"}
