"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""
import pytest
from urllib.parse import quote


def test_remove_existing_participant_success(client, test_activities):
    """Test successfully removing an existing participant."""
    response = client.delete("/activities/Chess Club/participants/player1@test.edu")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Removed player1@test.edu from Chess Club"
    assert "player1@test.edu" not in test_activities["Chess Club"]["participants"]


def test_remove_nonexistent_activity_returns_404(client, test_activities):
    """Test removing participant from non-existent activity returns 404."""
    response = client.delete("/activities/Fake Club/participants/student@test.edu")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_remove_nonexistent_participant_returns_404(client, test_activities):
    """Test removing non-existent participant returns 404."""
    response = client.delete("/activities/Drama Club/participants/notaparticipant@test.edu")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Participant not found"


def test_remove_from_empty_activity_returns_404(client, test_activities):
    """Test removing participant from activity with no participants."""
    response = client.delete("/activities/Empty Club/participants/student@test.edu")
    
    assert response.status_code == 404


def test_remove_only_participant(client, test_activities):
    """Test removing the only participant from an activity."""
    response = client.delete("/activities/Drama Club/participants/actor1@test.edu")
    
    assert response.status_code == 200
    assert test_activities["Drama Club"]["participants"] == []


def test_remove_one_of_multiple_participants(client, test_activities):
    """Test removing one participant when multiple are registered."""
    response = client.delete("/activities/Chess Club/participants/player1@test.edu")
    
    assert response.status_code == 200
    assert "player1@test.edu" not in test_activities["Chess Club"]["participants"]
    assert "player2@test.edu" in test_activities["Chess Club"]["participants"]


def test_remove_then_re_signup_same_participant(client, test_activities):
    """Test that a removed participant can sign up again."""
    # Remove participant
    response1 = client.delete("/activities/Drama Club/participants/actor1@test.edu")
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post("/activities/Drama Club/signup?email=actor1@test.edu")
    assert response2.status_code == 200
    assert "actor1@test.edu" in test_activities["Drama Club"]["participants"]


def test_remove_with_special_characters_in_email(client, test_activities):
    """Test removing participant with special characters in email."""
    # First, sign up someone with special email
    email = "user+test@example.edu"
    client.post(f"/activities/Drama Club/signup?email={quote(email)}")
    
    # Then remove them
    response = client.delete(f"/activities/Drama Club/participants/{quote(email)}")
    assert response.status_code == 200
    assert email not in test_activities["Drama Club"]["participants"]


def test_remove_multiple_participants_sequentially(client, test_activities):
    """Test removing multiple participants in sequence."""
    initial_count = len(test_activities["Chess Club"]["participants"])
    
    response1 = client.delete("/activities/Chess Club/participants/player1@test.edu")
    assert response1.status_code == 200
    
    response2 = client.delete("/activities/Chess Club/participants/player2@test.edu")
    assert response2.status_code == 200
    
    assert len(test_activities["Chess Club"]["participants"]) == initial_count - 2
    assert test_activities["Chess Club"]["participants"] == []
