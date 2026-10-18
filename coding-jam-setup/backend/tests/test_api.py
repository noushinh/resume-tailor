from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from models import BulletPair, TailorResponse

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "resume-tailor"}


def test_tailor_endpoint_success():
    fake_response = TailorResponse(
        bullets=[
            BulletPair(
                id="b-1",
                original="Managed social media accounts",
                tailored="Spearheaded social brand strategy reaching 1.2M impressions and lifting engagement by 42%",
                action_verb="Spearheaded",
                impact_tag="⚡ Action Verb Upgraded",
                matched_keyword="Social Media Strategy"
            )
        ],
        role_summary="Tailored for Growth Marketing Specialist.",
        total_upgraded=1,
    )

    with patch("main.tailor_resume_bullets", return_value=fake_response):
        payload = {
            "resume_text": "• Managed social media accounts and created weekly marketing content.",
            "job_description": "Seeking Growth Marketing Specialist with proven social brand track record."
        }
        response = client.post("/api/tailor", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_upgraded"] >= 1
        bullet = data["bullets"][0]
        assert bullet["original"] != ""
        assert bullet["tailored"] != ""
        assert bullet["action_verb"] != ""
        assert bullet["impact_tag"] != ""
        assert "Spearheaded" in bullet["tailored"]


def test_tailor_endpoint_validation_error():
    # Empty body
    response = client.post("/api/tailor", json={})
    assert response.status_code == 422

    # Strings too short (< 20 chars)
    response_short = client.post("/api/tailor", json={"resume_text": "Too short", "job_description": "Too short"})
    assert response_short.status_code in (400, 422)
