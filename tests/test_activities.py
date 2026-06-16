"""
Tests for the GET /activities endpoint.
"""
import pytest


def test_get_activities_returns_all_activities(client, test_activities):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 3
    assert "Chess Club" in activities
    assert "Drama Club" in activities
    assert "Empty Club" in activities


def test_get_activities_has_correct_structure(client, test_activities):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    activity = activities["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_shows_current_participants(client, test_activities):
    """Test that GET /activities shows current participants list."""
    response = client.get("/activities")
    activities = response.json()
    
    assert activities["Chess Club"]["participants"] == ["player1@test.edu", "player2@test.edu"]
    assert activities["Drama Club"]["participants"] == ["actor1@test.edu"]
    assert activities["Empty Club"]["participants"] == []


def test_get_activities_consistency_after_signup(client, test_activities):
    """Test that GET /activities reflects signup changes."""
    # Sign up a new participant
    client.post("/activities/Drama Club/signup?email=newactor@test.edu")
    
    # Fetch activities and verify the new participant is listed
    response = client.get("/activities")
    activities = response.json()
    
    assert "newactor@test.edu" in activities["Drama Club"]["participants"]
    assert len(activities["Drama Club"]["participants"]) == 2
