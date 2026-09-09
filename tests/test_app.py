from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activities["Soccer Team"]["participants"] = ["student@mergington.edu"]

    # Act
    response = client.delete("/activities/Soccer%20Team/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Removed student@mergington.edu from Soccer Team"
    assert "student@mergington.edu" not in activities["Soccer Team"]["participants"]


def test_signup_rejects_overbooked_activity():
    # Arrange
    activities["Chess Club"]["participants"] = [
        "a@example.com",
        "b@example.com",
        "c@example.com",
        "d@example.com",
        "e@example.com",
        "f@example.com",
        "g@example.com",
        "h@example.com",
        "i@example.com",
        "j@example.com",
        "k@example.com",
        "l@example.com",
    ]

    # Act
    response = client.post("/activities/Chess%20Club/signup?email=new@example.com")

    # Assert
    assert response.status_code == 400
    assert "maximum number of participants" in response.json()["detail"].lower()
