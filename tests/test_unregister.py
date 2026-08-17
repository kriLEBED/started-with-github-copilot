"""
Tests for DELETE /activities/{activity_name}/unregister endpoint
Testing student unregistration from activities
"""
import pytest
from src.app import activities


def test_unregister_success(test_client):
    """
    AAA Pattern:
    - Arrange: Student currently registered for activity
    - Act: DELETE /activities/{activity}/unregister?email={email}
    - Assert: Response 200, student removed from participants list
    """
    # Arrange
    activity = "Chess Club"
    email = activities["Chess Club"]["participants"][0]  # Get existing participant
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]


def test_unregister_decrements_participant_count(test_client):
    """
    AAA Pattern:
    - Arrange: Get initial participant count
    - Act: DELETE unregister request
    - Assert: Participant count decremented by 1
    """
    # Arrange
    activity = "Programming Class"
    email = activities["Programming Class"]["participants"][0]
    initial_count = len(activities["Programming Class"]["participants"])
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert len(activities["Programming Class"]["participants"]) == initial_count - 1


def test_unregister_not_registered_student(test_client):
    """
    AAA Pattern:
    - Arrange: Student not in activity participants
    - Act: DELETE /activities/{activity}/unregister?email={email}
    - Assert: Response 400 with error detail
    """
    # Arrange
    activity = "Gym Class"
    email = "notregistered@mergington.edu"
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_activity_not_found(test_client):
    """
    AAA Pattern:
    - Arrange: Non-existent activity
    - Act: DELETE /activities/{nonexistent}/unregister?email={email}
    - Assert: Response 404 with error detail
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_response_message_format(test_client):
    """
    AAA Pattern:
    - Arrange: Student and activity
    - Act: DELETE unregister request
    - Assert: Response message contains correct format
    """
    # Arrange
    activity = "Basketball Team"
    email = activities["Basketball Team"]["participants"][0]
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    message = response.json()["message"]
    assert email in message
    assert activity in message
    assert "Unregistered" in message


@pytest.mark.parametrize("activity", [
    "Tennis Club",
    "Art Class",
    "Drama Club"
])
def test_unregister_multiple_activities(test_client, activity):
    """
    AAA Pattern:
    - Arrange: Different activities (parametrized), with their existing participants
    - Act: DELETE unregister from each activity
    - Assert: Student removed from each activity
    
    Uses parametrization to test unregister from multiple activities
    """
    # Arrange
    email = activities[activity]["participants"][0]
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_then_signup_again(test_client):
    """
    AAA Pattern:
    - Arrange: Student registered for activity
    - Act: DELETE unregister, then POST signup again
    - Assert: Student can re-register after unregistering
    """
    # Arrange
    activity = "Robotics Club"
    email = activities["Robotics Club"]["participants"][0]
    
    # Act - unregister
    unregister_response = test_client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    # Act - signup again
    signup_response = test_client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert email in activities["Robotics Club"]["participants"]
