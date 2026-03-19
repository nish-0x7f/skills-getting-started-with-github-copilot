"""
Integration tests for DELETE /activities/{name}/signup endpoint using AAA pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities."""
    
    def test_unregister_existing_participant_succeeds(self, client):
        """
        Test successful unregistration of an existing participant.
        
        Arrange: TestClient, fresh app state, existing participant
        Act: Make DELETE request to unregister endpoint
        Assert: Verify status code 200 and student removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Existing participant
        
        # Verify student is initially enrolled
        activities_before = client.get("/activities").json()
        assert student_email in activities_before[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"
        
        # Verify student was actually removed
        activities_after = client.get("/activities").json()
        assert student_email not in activities_after[activity_name]["participants"]
    
    def test_unregister_returns_404_for_nonexistent_activity(self, client):
        """
        Test that unregister fails with 404 for non-existent activity.
        
        Arrange: TestClient, fresh app state, non-existent activity
        Act: Make DELETE request with invalid activity name
        Assert: Verify status code 404 and error message
        """
        # Arrange
        nonexistent_activity = "Fake Activity"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_student_not_enrolled_fails(self, client):
        """
        Test that unregister fails when student is not enrolled in activity.
        
        Arrange: TestClient, fresh app state, student not in activity
        Act: Attempt to unregister student not enrolled
        Assert: Verify appropriate error response
        """
        # Arrange
        activity_name = "Basketball Team"
        student_not_enrolled = "notenrolled@test.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_not_enrolled}
        )
        
        # Assert - App should return 400 error
        assert response.status_code == 400
    
    def test_unregister_then_signup_again_works(self, client):
        """
        Test that a student can sign up again after unregistering.
        
        Arrange: TestClient, fresh app state, existing participant
        Act: Unregister, then sign up again
        Assert: Both operations succeed and student is enrolled
        """
        # Arrange
        activity_name = "Tennis Club"
        student_email = "ryan@mergington.edu"  # Existing participant
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Verify unregistered
        activities_after_unregister = client.get("/activities").json()
        assert student_email not in activities_after_unregister[activity_name]["participants"]
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        
        # Verify student is re-enrolled
        activities_final = client.get("/activities").json()
        assert student_email in activities_final[activity_name]["participants"]
    
    def test_unregister_multiple_participants_from_activity(self, client):
        """
        Test unregistering multiple participants from same activity.
        
        Arrange: TestClient, fresh app state with multiple participants
        Act: First unregister one participant, then another
        Assert: Both removed and activity still has remaining participants
        """
        # Arrange
        activity_name = "Music Ensemble"
        student1 = "grace@mergington.edu"
        student2 = "james@mergington.edu"
        
        # Act - Unregister first student
        response1 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student1}
        )
        
        # Act - Unregister second student
        response2 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": student2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are removed
        activities_final = client.get("/activities").json()
        participants = activities_final[activity_name]["participants"]
        assert student1 not in participants
        assert student2 not in participants
        assert len(participants) == 0  # No one left in this activity
