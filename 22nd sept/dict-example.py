student = {
    "name": "Riju",
    "age" : 22,
    "course" : "AIML"
}
student["grade"] = "A" # adding key
student["age"] = 67 # updating value of a key

# Removing a key
student.pop("course")
del student["grade"]

# print(student["age"]) # accessing by key
# print(student.get("grade")) # accessing by method
# print(student)

#For loop for dict
for key, value in student.items():
    print(f"{key} : {value}")

