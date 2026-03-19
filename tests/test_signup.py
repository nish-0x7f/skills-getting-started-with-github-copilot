"""
Integration tests for POST /activities/{name}/signup endpoint using AAA pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities."""
    
    def test_signup_successful_with_new_email(self, client):
        """
        Test successful signup of a new student to an activity.
        
        Arrange: TestClient, fresh app state, and student email
        Act: Make POST request to signup endpoint
        Assert: Verify status code 200 and student added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
        
        # Verify student was actually added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student_email in activities[activity_name]["participants"]
    
    def test_signup_returns_404_for_nonexistent_activity(self, client):
        """
        Test that signup fails with 404 for non-existent activity.
        
        Arrange: TestClient, fresh app state, and invalid activity name
        Act: Make POST request with non-existent activity
        Assert: Verify status code 404 and appropriate error message
        """
        # Arrange
        nonexistent_activity = "Nonexistent Activity"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_returns_400_for_duplicate_enrollment(self, client):
        """
        Test that signup fails with 400 when student already enrolled.
        
        Arrange: TestClient, fresh app state, existing participant
        Act: Attempt to sign up same student twice
        Assert: Verify status code 400 and duplicate signup prevented
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already participant
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    
    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Test that multiple different students can sign up for same activity.
        
        Arrange: TestClient, fresh app state, two different students
        Act: Sign up first student, then second student
        Assert: Both students successfully added to participants
        """
        # Arrange
        activity_name = "Art Studio"
        student1_email = "student1@test.edu"
        student2_email = "student2@test.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1_email}
        )
        
        # Act - Second signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both students are enrolled
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity_name]["participants"]
        assert student1_email in participants
        assert student2_email in participants
    
    def test_signup_student_to_same_activity_twice_fails(self, client):
        """
        Test that a student cannot sign up twice to the same activity.
        
        Arrange: TestClient, fresh app state, new student
        Act: Sign up student once successfully, then attempt again
        Assert: Second attempt fails with 400
        """
        # Arrange
        activity_name = "Science Club"
        student_email = "unique@test.edu"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Act - Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Student already signed up for this activity"
