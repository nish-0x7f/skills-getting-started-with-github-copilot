"""
Pytest configuration and shared fixtures for FastAPI tests.

Provides:
- app: Fresh FastAPI application instance
- client: TestClient for making HTTP requests
- activities_fixture: Clean activities data for each test
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def fresh_app():
    """
    Provide a fresh app instance with reset activities for each test.
    
    Arrange: Initialize the app with clean state
    """
    # Import here to get a fresh reference each test
    from src import app as app_module
    
    # Reset activities to known state
    clean_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ryan@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and digital art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Perform in school orchestra and chamber ensembles",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "james@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["avery@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM topics",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Replace app's activities with clean state
    app_module.activities.clear()
    app_module.activities.update(clean_activities)
    
    return app_module.app


@pytest.fixture
def client(fresh_app):
    """
    Provide a TestClient for making HTTP requests to the app.
    
    Arrange: Initialize TestClient with fresh app instance
    """
    return TestClient(fresh_app)


@pytest.fixture
def activity_with_capacity():
    """
    Provide a test activity at near capacity for testing edge cases.
    
    Arrange: Return a sample activity configuration for capacity tests
    """
    return {
        "name": "Small Group",
        "description": "A small group activity",
        "schedule": "Daily",
        "max_participants": 2,
        "participants": ["user1@test.edu", "user2@test.edu"]
    }
