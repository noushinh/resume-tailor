"""Resume Tailor — FastAPI server."""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from generator import tailor_resume_bullets
from models import TailorRequest, TailorResponse

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Verify configuration at startup."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Startup] WARNING: GEMINI_API_KEY environment variable is not set.")
    else:
        print(f"[Startup] GEMINI_API_KEY loaded successfully ({api_key[:6]}...).")
    yield


app = FastAPI(title="Resume Tailor", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/tailor", response_model=TailorResponse)
async def tailor_endpoint(request: TailorRequest):
    """Analyze resume bullets against target job description and return tailored bullets."""
    if len(request.resume_text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Resume text must be at least 20 characters.",
        )
    if len(request.job_description.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Job description must be at least 20 characters.",
        )

    try:
        response = tailor_resume_bullets(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Check for missing API key or connection errors
        error_msg = str(e)
        if "API_KEY" in error_msg or "credentials" in error_msg.lower():
            raise HTTPException(
                status_code=502,
                detail="Gemini API credentials not configured or invalid.",
            )
        raise HTTPException(
            status_code=502,
            detail=f"AI generation failed: {error_msg}",
        )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "resume-tailor"}


# Mount frontend static files if directory exists (must be last)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
