from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_endpoint_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert "message" in body
    assert email not in activities[activity_name]["participants"]


def test_unregister_endpoint_rejects_unknown_student():
    activity_name = "Chess Club"
    email = "student-not-signed-up@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 404, response.text
