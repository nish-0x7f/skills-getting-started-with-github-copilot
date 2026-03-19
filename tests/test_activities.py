"""
Integration tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        Arrange: TestClient and fresh app state (via fixtures)
        Act: Make GET request to /activities
        Assert: Verify status code 200 and response contains all activities
        """
        # Arrange
        expected_activities_count = 9
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activities_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_returns_valid_structure(self, client):
        """
        Test that each activity has required fields.
        
        Arrange: TestClient and fresh app state (via fixtures)
        Act: Make GET request to /activities
        Assert: Verify each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity {activity_name} missing required fields"
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_shows_current_participants(self, client):
        """
        Test that participants list reflects current state.
        
        Arrange: TestClient and fresh app state (via fixtures)
        Act: Make GET request to /activities
        Assert: Verify Chess Club has initial participants
        """
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert chess_club["participants"] == expected_chess_participants
        assert len(chess_club["participants"]) == 2
