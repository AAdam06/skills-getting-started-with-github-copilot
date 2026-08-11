from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert expected_activity in json_data
    assert "participants" in json_data[expected_activity]


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400():
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    url = f"/activities/{activity_name}/signup?email={email}"
    expected_count = client.get("/activities").json()[activity_name]["participants"].count(email)

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert client.get("/activities").json()[activity_name]["participants"].count(email) == expected_count


def test_signup_with_url_encoded_activity_name():
    # Arrange
    activity_name = "Science Club"
    email = "encodedstudent@mergington.edu"
    url = "/activities/Science%20Club/signup?email=encodedstudent%40mergington.edu"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"
    url = f"/activities/{activity_name}/participants/{email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"
    url = f"/activities/{activity_name}/participants/{email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
