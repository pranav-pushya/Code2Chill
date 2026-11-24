from fastapi.testclient import TestClient

from app.main import app


def test_submit_valid_inquiry():
    client = TestClient(app)
    response = client.post(
        "/api/inquiries",
        json={
            "full_name": "Jasleen Kaur",
            "email": "jasleen@chitkara.edu.in",
            "category": "events",
            "message": "When is the next hackathon registration opening?",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"


def test_submit_invalid_inquiry_email():
    client = TestClient(app)
    response = client.post(
        "/api/inquiries",
        json={
            "full_name": "Jasleen Kaur",
            "email": "invalid-email-format",
            "category": "events",
            "message": "When is the next hackathon?",
        },
    )
    assert response.status_code == 422
