import json
from unittest.mock import MagicMock
import pytest
from generator import parse_gemini_json_response, tailor_resume_bullets
from models import TailorResponse


def test_gemini_response_parser():
    raw_json = json.dumps({
        "role_summary": "Tailored for Senior Systems Architect.",
        "bullets": [
            {
                "id": "b-1",
                "original": "Managed servers and network uptime.",
                "tailored": "Architected resilient multi-region infrastructure maintaining 99.99% availability.",
                "action_verb": "Architected",
                "impact_tag": "⚡ Action Verb Upgraded",
                "matched_keyword": "Infrastructure Reliability"
            }
        ]
    })

    # Test direct JSON
    response = parse_gemini_json_response(raw_json)
    assert isinstance(response, TailorResponse)
    assert response.total_upgraded == 1
    assert response.bullets[0].action_verb == "Architected"
    assert response.bullets[0].matched_keyword == "Infrastructure Reliability"

    # Test JSON wrapped in markdown fences
    fenced_json = f"```json\n{raw_json}\n```"
    fenced_response = parse_gemini_json_response(fenced_json)
    assert fenced_response.total_upgraded == 1
    assert fenced_response.bullets[0].action_verb == "Architected"


def test_tailor_resume_bullets_with_mock_client():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "role_summary": "Tailored for Lead Software Engineer.",
        "bullets": [
            {
                "id": "b-1",
                "original": "Built user interface for checkout.",
                "tailored": "Engineered high-converting checkout workflow reducing cart abandonment by 18%.",
                "action_verb": "Engineered",
                "impact_tag": "📈 Metric Quantified",
                "matched_keyword": "Frontend UX"
            }
        ]
    })
    mock_client.models.generate_content.return_value = mock_response

    resume = "• Built user interface for checkout."
    job = "Looking for a Lead Software Engineer to overhaul e-commerce checkout systems."

    result = tailor_resume_bullets(resume, job, client=mock_client)
    assert result.total_upgraded == 1
    assert result.bullets[0].action_verb == "Engineered"
    assert "cart abandonment" in result.bullets[0].tailored
    mock_client.models.generate_content.assert_called_once()
