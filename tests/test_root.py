"""
Tests for GET / endpoint
Testing the root redirect to /static/index.html
"""
import pytest


def test_root_redirect(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient ready
    - Act: GET /
    - Assert: Response is 307 redirect to /static/index.html
    """
    # Act
    response = test_client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient ready
    - Act: GET / with follow_redirects=True
    - Assert: Final response indicates successful navigation
    """
    # Act
    response = test_client.get("/", follow_redirects=True)
    
    # Assert
    # After following redirect, we get static files or 200 OK
    # (actual response depends on static file handling)
    assert response.status_code == 200


def test_root_redirect_location_header(test_client):
    """
    AAA Pattern:
    - Arrange: TestClient ready
    - Act: GET / and check Location header
    - Assert: Location header points to /static/index.html
    """
    # Act
    response = test_client.get("/", follow_redirects=False)
    
    # Assert
    assert "location" in response.headers
    location = response.headers["location"]
    assert location == "/static/index.html"
    assert location.startswith("/static/")
