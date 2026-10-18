import json
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import BulletPair, TailorResponse
from prompts import SYSTEM_PROMPT
from text_utils import extract_bullets

load_dotenv()


def create_gemini_client() -> genai.Client:
    """Create a fresh Gemini client for each request."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )


def parse_gemini_json_response(response_text: str) -> TailorResponse:
    """Parse and validate raw JSON response text from Gemini into TailorResponse."""
    text = response_text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    data = json.loads(text)

    bullets_raw = data.get("bullets", [])
    if not isinstance(bullets_raw, list) or len(bullets_raw) == 0:
        raise ValueError("Model returned empty or invalid bullets list.")

    bullets: list[BulletPair] = []
    for idx, b in enumerate(bullets_raw, start=1):
        bullets.append(
            BulletPair(
                id=str(b.get("id", f"b-{idx}")),
                original=str(b.get("original", "")).strip(),
                tailored=str(b.get("tailored", "")).strip(),
                action_verb=str(b.get("action_verb", "Enhanced")).strip(),
                impact_tag=str(b.get("impact_tag", "⚡ Action Verb Upgraded")).strip(),
                matched_keyword=b.get("matched_keyword"),
            )
        )

    role_summary = data.get(
        "role_summary", "Tailored resume bullets aligned with target role."
    )

    return TailorResponse(
        bullets=bullets,
        role_summary=role_summary,
        total_upgraded=len(bullets),
    )


def tailor_resume_bullets(
    resume_text: str,
    job_description: str,
    client: Optional[genai.Client] = None,
) -> TailorResponse:
    """Extract bullets, query Gemini for tailored rewrites, and return structured TailorResponse."""
    extracted = extract_bullets(resume_text)
    if not extracted:
        raise ValueError("No bullet points or experience could be extracted from resume text.")

    bullets_formatted = "\n".join(f"- {b}" for b in extracted)
    user_prompt = f"""TARGET JOB DESCRIPTION:
\"\"\"{job_description.strip()[:10000]}\"\"\"

CANDIDATE'S CURRENT RESUME BULLETS:
\"\"\"{bullets_formatted[:10000]}\"\"\"

Rewrite each candidate bullet point to maximize relevance, quantified impact metrics, and muscular action verbs matching the target job description. Return valid JSON only."""

    if client is None:
        client = create_gemini_client()

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    response = client.models.generate_content(
        model=model_name,
        contents=[
            {
                "role": "user",
                "parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_prompt}],
            }
        ],
        config=types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
        ),
    )

    return parse_gemini_json_response(response.text)
