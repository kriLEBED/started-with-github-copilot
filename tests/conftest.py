"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store a pristine copy of activities at module load time for test isolation
_PRISTINE_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def test_client():
    """Provide a FastAPI TestClient for testing API endpoints"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset the global activities dict before each test.
    This ensures test isolation - changes in one test don't affect others.
    This fixture runs for every test without being explicitly requested.
    """
    # Store original state (in case activities were modified)
    original_state = copy.deepcopy(activities)
    
    # Clear and restore pristine activities for this test
    activities.clear()
    activities.update(copy.deepcopy(_PRISTINE_ACTIVITIES))
    
    # Yield to run the test
    yield
    
    # Cleanup: restore to original state after test
    activities.clear()
    activities.update(original_state)
