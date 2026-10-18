import pytest
from text_utils import extract_bullets


def test_extract_bullets_standard():
    text = """
    • Managed social media accounts and created marketing content.
    - Built user interface for checkout system.
    * Fixed bugs reported by clients in web application.
    1. Led weekly sprint planning sessions.
    2. Mentored junior developers.
    """
    bullets = extract_bullets(text)
    assert len(bullets) == 5
    assert bullets[0] == "Managed social media accounts and created marketing content."
    assert bullets[1] == "Built user interface for checkout system."
    assert bullets[2] == "Fixed bugs reported by clients in web application."
    assert bullets[3] == "Led weekly sprint planning sessions."
    assert bullets[4] == "Mentored junior developers."


def test_extract_bullets_unstructured():
    text = """First paragraph describing software engineering work at prior company.

Second paragraph detailing contributions to database migration and query optimizations."""
    bullets = extract_bullets(text)
    assert len(bullets) == 2
    assert "First paragraph" in bullets[0]
    assert "Second paragraph" in bullets[1]


def test_extract_bullets_empty_or_whitespace():
    assert extract_bullets("") == []
    assert extract_bullets("   \n\t  \r\n  ") == []
