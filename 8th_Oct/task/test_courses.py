from fastapi.testclient import TestClient
from courses_api import app

client = TestClient(app)

# Test 1
def test_add_course():
    new_course = {"id": 2, "title": "ML Basics", "duration": 60, "fee": 5000, "is_active": True}
    response = client.post("/courses", json=new_course)
    assert response.status_code == 201
    assert response.json()["title"] == "ML Basics"

def test_duplicate_course_found():
    new_course = {"id": 1, "title": "BERT", "duration": 30, "fee": 2000, "is_active": True}
    response = client.post("/courses/", json=new_course)
    assert response.status_code == 400
    assert response.json()['detail'] == "Course ID already exists"


def test_validation_error_corrected():
    new_course = {"id": 2, "title": "AI", "duration": 0, "fee": -500, "is_active": True}

    # Corrected URL: /courses (no trailing slash)
    response = client.post("/courses", json=new_course)
    assert response.status_code == 422
    response_text = response.text
    assert "greater_than" in response_text


def test_get_all_courses_format():
    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("title" in course for course in data)
    assert all("id" in course for course in data)
    assert all("fee" in course for course in data)
    assert all("duration" in course for course in data)
    assert all("is_active" in course for course in data)