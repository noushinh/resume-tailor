import pytest
from pydantic import ValidationError
from models import TailorRequest, BulletPair, TailorResponse


def test_tailor_request_validation():
    # Valid request
    valid = TailorRequest(
        resume_text="Managed infrastructure across 5 regions successfully.",
        job_description="Seeking a Senior DevOps engineer with AWS expertise.",
    )
    assert valid.resume_text.startswith("Managed")

    # Invalid: resume_text too short (< 20 chars)
    with pytest.raises(ValidationError):
        TailorRequest(
            resume_text="Too short",
            job_description="Seeking a Senior DevOps engineer with AWS expertise.",
        )

    # Invalid: job_description too short (< 20 chars)
    with pytest.raises(ValidationError):
        TailorRequest(
            resume_text="Managed infrastructure across 5 regions successfully.",
            job_description="Short job",
        )

    # Invalid: fields exceed maximum limits (> 15000 chars)
    with pytest.raises(ValidationError):
        TailorRequest(
            resume_text="x" * 15001,
            job_description="Seeking a Senior DevOps engineer with AWS expertise.",
        )


def test_bullet_pair_and_response_models():
    pair = BulletPair(
        id="b-1",
        original="Managed social media accounts",
        tailored="Orchestrated social campaigns driving 40% user growth",
        action_verb="Orchestrated",
        impact_tag="📈 Metric Quantified",
        matched_keyword="Social Media Marketing",
    )
    assert pair.action_verb == "Orchestrated"

    resp = TailorResponse(
        bullets=[pair],
        role_summary="Tailored for marketing leadership role.",
        total_upgraded=1,
    )
    assert resp.total_upgraded == 1
    assert len(resp.bullets) == 1
