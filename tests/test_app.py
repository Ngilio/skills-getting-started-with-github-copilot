import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert "Basketball Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Math Olympiad/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Math Olympiad" in response.json()["message"]

def test_signup_for_activity_already_signed_up():
    # User already in Soccer Team
    response = client.post("/activities/Soccer Team/signup", params={"email": "lucas@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # Add user, then remove
    client.post("/activities/Drama Club/signup", params={"email": "removeuser@mergington.edu"})
    response = client.post("/activities/Drama Club/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 200
    assert "has been removed from Drama Club" in response.json()["message"]

def test_unregister_from_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_participant_not_found():
    response = client.post("/activities/Art Workshop/unregister", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
