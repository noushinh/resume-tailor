import re
from typing import List

BULLET_PREFIX_RE = re.compile(
    r"^\s*(?:[\u2022\u2023\u25E6\u2043\u2219\*\-\+]|\d+[\.\)])\s+"
)


def extract_bullets(raw_text: str) -> List[str]:
    """Extract discrete bullet points or experience segments from pasted text.

    Handles standard bullet glyphs (•, -, *, 1.) and unstructured multiline text.
    """
    if not raw_text or not raw_text.strip():
        return []

    raw_lines = raw_text.strip().splitlines()
    bullets: List[str] = []

    # Check if lines have bullet prefixes
    has_explicit_bullets = any(
        BULLET_PREFIX_RE.match(line) for line in raw_lines if line.strip()
    )

    if has_explicit_bullets:
        current_bullet: List[str] = []
        for line in raw_lines:
            line_str = line.strip()
            if not line_str:
                continue
            match = BULLET_PREFIX_RE.match(line_str)
            if match:
                if current_bullet:
                    bullets.append(" ".join(current_bullet).strip())
                    current_bullet = []
                cleaned = line_str[match.end():].strip()
                if cleaned:
                    current_bullet.append(cleaned)
            else:
                if current_bullet:
                    current_bullet.append(line_str)
                else:
                    bullets.append(line_str)
        if current_bullet:
            bullets.append(" ".join(current_bullet).strip())
    else:
        # Check if text has double newlines (paragraphs)
        if "\n\n" in raw_text:
            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            for p in paragraphs:
                p_lines = [l.strip() for l in p.splitlines() if l.strip()]
                bullets.extend(p_lines)
        else:
            bullets = [l.strip() for l in raw_lines if l.strip()]

    return [b for b in bullets if b.strip()]
