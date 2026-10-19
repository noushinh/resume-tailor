⚡ Resume Tailor (restated again once clicked on folder. Please click on folder to access all necessary information regarding Resume Tailor. Thank you 😊!!)

Transform passive resume bullets into quantified, high-impact statements matched to your target role.

Resume Tailor is a focused web application designed to eliminate generic, passive phrasing from your resume. By comparing your existing bullet points against a target job description, it instantly generates tailored rewrites powered by Google Gemini AI — leading with punchy action verbs, quantified metrics, and matched competencies in a side-by-side comparison.
📖 Source of Truth: Design Documents

The system design, product requirements, and user experience were engineered using rigorous design doc skills. Anyone looking to understand the core rationale, boundaries, and technical specifications should read:

    product.md — Product Requirements Document (PRD): Explains target users, the core contract (I/O), the magical moment, ruthless scope exclusions, and the signature coaching tags.
    ui.md — UX Design Specification: Covers the single-canvas interface, split dual-input grid, interactive comparison matrix, states (loading, empty, error), and accessibility.
    engineering.md — Engineering Architecture Doc: Details the FastAPI + Google GenAI SDK architecture, structured JSON schemas, latency targets, and comprehensive testing strategy.

🚀 Getting Started
Prerequisites

    Python 3.11+
    uv (fast Python package manager)
    A Gemini API Key from Google AI Studio

1. Installation

Clone the repository and install dependencies using uv:

cd backend
uv sync --extra test

2. Environment Configuration

Copy the example environment file and configure your Gemini API key:

cp .env.example .env

Edit backend/.env with your settings:

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash

    Note: .env is listed in .gitignore and is never tracked by version control.

3. Running the Development Server

Start the FastAPI application with live reloading enabled:

cd backend
uv run uvicorn main:app --reload --port 8000

Once started, open your browser and navigate to:

👉 http://localhost:8000

The backend automatically serves the frontend interface as static files from / while routing API requests to /api/tailor and /api/health.
🧪 Running Automated Tests

Run the full automated test suite (unit and integration tests) using pytest:

cd backend
uv run pytest -v

All external LLM calls are mocked in the test suite to ensure deterministic, fast, and free verification.
