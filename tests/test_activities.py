"""
Tests for GET /activities endpoint
Testing the retrieval of all available activities
"""
import pytest


def test_get_activities_returns_all_activities(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient is ready with fresh activities data
    - Act: GET /activities
    - Assert: Response contains all activities with correct structure
    """
    # Act
    response = test_client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities_data = response.json()
    
    # Verify all expected activities are present
    assert "Chess Club" in activities_data
    assert "Programming Class" in activities_data
    assert "Gym Class" in activities_data
    assert "Basketball Team" in activities_data
    assert "Tennis Club" in activities_data
    assert "Art Class" in activities_data
    assert "Drama Club" in activities_data
    assert "Robotics Club" in activities_data
    assert "Debate Team" in activities_data


def test_get_activities_response_structure(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient is ready
    - Act: GET /activities
    - Assert: Each activity has required fields (description, schedule, max_participants, participants)
    """
    # Act
    response = test_client.get("/activities")
    activities_data = response.json()
    
    # Assert - verify structure of first activity
    chess_club = activities_data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
    assert isinstance(chess_club["max_participants"], int)


def test_get_activities_participants_count(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient with known participant data
    - Act: GET /activities
    - Assert: Participant counts match expected values
    """
    # Act
    response = test_client.get("/activities")
    activities_data = response.json()
    
    # Assert - verify initial participant counts
    assert len(activities_data["Chess Club"]["participants"]) == 2
    assert len(activities_data["Programming Class"]["participants"]) == 2
    assert len(activities_data["Gym Class"]["participants"]) == 2


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Basketball Team",
    "Tennis Club",
    "Art Class",
    "Drama Club",
    "Robotics Club",
    "Debate Team"
])
def test_get_activities_all_activities_have_valid_data(test_client, activity_name):
    """
    AAA Pattern:
    - Arrange: TestClient ready, parametrized with each activity
    - Act: GET /activities
    - Assert: Each activity has non-empty description and valid max_participants
    
    Uses parametrization to test all activities efficiently
    """
    # Act
    response = test_client.get("/activities")
    activities_data = response.json()
    
    # Assert
    activity = activities_data[activity_name]
    assert activity["description"], f"{activity_name} should have a description"
    assert activity["schedule"], f"{activity_name} should have a schedule"
    assert activity["max_participants"] > 0, f"{activity_name} should have positive max_participants"
    assert isinstance(activity["participants"], list), f"{activity_name} participants should be a list"
