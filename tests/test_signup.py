"""
Tests for POST /activities/{activity_name}/signup endpoint
Testing student registration for activities
"""
import pytest
from src.app import activities


def test_signup_success(test_client):
    """
    AAA Pattern:
    - Arrange: New student email and existing activity
    - Act: POST /activities/{activity}/signup?email={email}
    - Assert: Response 200, student added to participants list
    """
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_duplicate_prevention(test_client):
    """
    AAA Pattern:
    - Arrange: Student already registered for activity
    - Act: POST same signup request again
    - Assert: Response 400 with error detail
    """
    # Arrange
    activity = "Chess Club"
    email = activities["Chess Club"]["participants"][0]  # Use existing participant
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(test_client):
    """
    AAA Pattern:
    - Arrange: Non-existent activity name
    - Act: POST /activities/{nonexistent}/signup?email={email}
    - Assert: Response 404 with error detail
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_increments_participant_count(test_client):
    """
    AAA Pattern:
    - Arrange: Get initial participant count
    - Act: POST signup request
    - Assert: Participant count incremented by 1
    """
    # Arrange
    activity = "Gym Class"
    email = "newgym@mergington.edu"
    initial_count = len(activities["Gym Class"]["participants"])
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert len(activities["Gym Class"]["participants"]) == initial_count + 1


@pytest.mark.parametrize("activity", [
    "Chess Club",
    "Programming Class",
    "Basketball Team"
])
def test_signup_multiple_activities(test_client, activity):
    """
    AAA Pattern:
    - Arrange: Different activities (parametrized)
    - Act: POST signup to each activity
    - Assert: Student successfully added to each
    
    Uses parametrization to test signup for multiple activities
    """
    # Arrange
    email = f"student.{activity}@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_response_message_format(test_client):
    """
    AAA Pattern:
    - Arrange: Student and activity
    - Act: POST signup request
    - Assert: Response message contains correct format
    """
    # Arrange
    activity = "Drama Club"
    email = "dramaticstudent@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    message = response.json()["message"]
    assert email in message
    assert activity in message
    assert "Signed up" in message
