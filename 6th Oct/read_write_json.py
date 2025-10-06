import json

student = {
    "name" : "Som",
    "age" : 22,
    "courses" : ["AI", "ML"],
    "marks" : {"AI":67, "ML":69}
}

# write a file into json
with open('student.json', 'w') as f:
    json.dump(student, f, indent=4)

# read from a json file
with open('student.json', 'r') as f:
    data = json.load(f)

# using the json file to obtain data
print(f"The subjects of {data['name']} are {data['courses']}")
print(f"{data['name']} got {data['marks']['AI']} in {data['courses'][0]}")