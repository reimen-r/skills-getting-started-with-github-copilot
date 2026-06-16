"""
Pytest configuration and shared fixtures for the API tests.
"""
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app


# Sample activities data for testing
SAMPLE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 2,
        "participants": ["player1@test.edu", "player2@test.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 3,
        "participants": ["actor1@test.edu"]
    },
    "Empty Club": {
        "description": "A club with no participants",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 5,
        "participants": []
    }
}


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def test_activities(monkeypatch):
    """
    Provide a fresh copy of test activities for each test.
    This prevents test pollution by resetting activities between tests.
    """
    activities_copy = deepcopy(SAMPLE_ACTIVITIES)
    monkeypatch.setattr("src.app.activities", activities_copy)
    return activities_copy
