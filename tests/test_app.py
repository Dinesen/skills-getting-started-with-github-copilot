import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    """Test root endpoint redirect to static interface (supports FR3)"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities():
    """Test retrieving list of activities with details (covers FR1, FR2)"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_for_activity():
    """Test successful signup and duplicate prevention (covers FR4, FR5, FR7, FR8)"""
    # Test successful signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Check that the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

    # Test signup when already signed up
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]


def test_signup_activity_not_found():
    """Test signup validation for non-existent activity (covers FR5)"""
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_activity_full():
    """Test signup prevention when activity is at capacity (covers FR6)"""
    # First, fill up an activity
    activity = "Tennis Club"
    max_participants = 8
    for i in range(max_participants - len(client.get("/activities").json()[activity]["participants"])):
        client.post(f"/activities/{activity}/signup", params={"email": f"user{i}@example.com"})

    # Now try to signup when full
    response = client.post(f"/activities/{activity}/signup", params={"email": "overflow@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Activity is full" in data["detail"]


def test_unregister_from_activity():
    """Test successful unregistration (covers FR10, FR11)"""
    # First signup
    client.post("/activities/Basketball/signup", params={"email": "unregister@example.com"})

    # Now unregister
    response = client.post("/activities/Basketball/unregister", params={"email": "unregister@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@example.com from Basketball" in data["message"]

    # Check removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Basketball"]["participants"]


def test_unregister_activity_not_found():
    """Test unregistration validation for non-existent activity (covers FR10)"""
    response = client.post("/activities/Nonexistent Activity/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up():
    """Test unregistration validation when student not signed up (covers FR10)"""
    response = client.post("/activities/Drama Club/unregister", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up for this activity" in data["detail"]