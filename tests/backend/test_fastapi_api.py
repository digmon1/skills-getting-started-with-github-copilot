from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities_returns_catalog():
    response = client.get("/activities")

    assert response.status_code == 200, response.text
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_endpoint_adds_new_student_to_activity():
    activity_name = "Soccer Team"
    email = "backend-api-student@mergington.edu"

    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert "message" in body
    assert email in activities[activity_name]["participants"]


def test_signup_endpoint_rejects_duplicate_student():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400, response.text
