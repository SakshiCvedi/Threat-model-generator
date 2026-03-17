import pytest
import os
from pathlib import Path
from app.renderer import render_terminal, render_markdown, render_pdf


# Sample threat model for all renderer tests
SAMPLE_THREAT_MODEL = {
    "system_name": "Test System",
    "overall_risk_score": 6,
    "trust_boundaries": ["Client to API", "API to Database"],
    "stride": {
        "spoofing": {
            "risk": "High",
            "threats": ["Token forgery"],
            "mitigations": ["Use strong signing"]
        },
        "tampering": {
            "risk": "Medium",
            "threats": ["SQL injection"],
            "mitigations": ["Parameterized queries"]
        },
        "repudiation": {
            "risk": "Low",
            "threats": ["No audit log"],
            "mitigations": ["Add logging"]
        },
        "information_disclosure": {
            "risk": "High",
            "threats": ["Data leak in logs"],
            "mitigations": ["Sanitize logs"]
        },
        "denial_of_service": {
            "risk": "Medium",
            "threats": ["No rate limiting"],
            "mitigations": ["Add rate limiter"]
        },
        "elevation_of_privilege": {
            "risk": "Critical",
            "threats": ["Missing RBAC"],
            "mitigations": ["Implement RBAC"]
        }
    },
    "top_3_actions": [
        "Add RBAC immediately",
        "Sanitize all log output",
        "Implement rate limiting"
    ]
}


# ─────────────────────────────────────────
# Test 1 — Terminal render doesn't crash
# ─────────────────────────────────────────

def test_render_terminal_runs_without_error():
    """Terminal renderer should run without throwing any exception"""
    try:
        render_terminal(SAMPLE_THREAT_MODEL)
    except Exception as e:
        pytest.fail(f"render_terminal raised an exception: {e}")


# ─────────────────────────────────────────
# Test 2 — Markdown file is created
# ─────────────────────────────────────────

def test_render_markdown_creates_file():
    """Markdown renderer should create a .md file in outputs/"""
    render_markdown(SAMPLE_THREAT_MODEL)

    # Check that at least one .md file exists in outputs/
    output_files = list(Path("outputs").glob("*.md"))
    assert len(output_files) > 0


# ─────────────────────────────────────────
# Test 3 — Markdown content is correct
# ─────────────────────────────────────────

def test_render_markdown_content():
    """Markdown output should contain system name and STRIDE categories"""
    content = render_markdown(SAMPLE_THREAT_MODEL)

    assert "Test System"  in content
    assert "Spoofing"     in content
    assert "Tampering"    in content
    assert "Top 3"        in content


# ─────────────────────────────────────────
# Test 4 — PDF file is created
# ─────────────────────────────────────────

def test_render_pdf_creates_file():
    """PDF renderer should create a .pdf file in outputs/"""
    render_pdf(SAMPLE_THREAT_MODEL)

    output_files = list(Path("outputs").glob("*.pdf"))
    assert len(output_files) > 0