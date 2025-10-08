from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test 1
def test_get_all_employees():
    response = client.get("/employees") # ACT
    assert response.status_code == 200 # Assert
    assert isinstance(response.json(), dict) # Assert

# Arrange ACT Assert -- AAA Pattern
# CICD - Continuous Integration COnt Deployment -- check in -- build -- test_case -- deployed to QA server

# Test 2
def test_add_employee():
    new_emp ={"id": 1, "name": "Rahul", "dept" : "HR", "salary": 56000.00}
    response = client.post("/employees", json = new_emp)
    assert response.status_code == 201
    assert response.json()["name"] == "Rahul"

# Test 3
def test_get_employee_by_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "RaONE"

# Test 4
def test_get_employee_not_found():
    response = client.get("/employees/88")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

# Test 5
def test_update_employee():
    up_emp = {"id": 1, "name": "Meena", "dept" : "AI", "salary": 50000.00}
    response = client.put("/employees/1", json = up_emp)
    assert response.status_code == 200
    assert response.json()["name"] == "Meena"

# Test 6
def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee Deleted Successfully"