from pydantic import BaseModel, Field
from typing import List, Optional


class TailorRequest(BaseModel):
    resume_text: str = Field(..., min_length=20, max_length=15000, description="Pasted resume text")
    job_description: str = Field(..., min_length=20, max_length=15000, description="Target job description")


class BulletPair(BaseModel):
    id: str = Field(..., description="Unique bullet identifier")
    original: str = Field(..., description="Original raw bullet point from resume")
    tailored: str = Field(..., description="Upgraded bullet point with action verbs and metrics")
    action_verb: str = Field(..., description="Strong action verb utilized (e.g., 'Spearheaded')")
    impact_tag: str = Field(..., description="Short tag explaining upgrade (e.g., '⚡ Action Verb', '📈 Metric Added')")
    matched_keyword: Optional[str] = Field(None, description="Target skill or requirement matched")


class TailorResponse(BaseModel):
    bullets: List[BulletPair]
    role_summary: str = Field(..., description="1-sentence synthesis of target role alignment")
    total_upgraded: int
