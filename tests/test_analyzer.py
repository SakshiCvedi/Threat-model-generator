import pytest
from unittest.mock import patch, MagicMock
from app.analyzer import generate_threat_model


# ─────────────────────────────────────────
# What is mocking?
# ─────────────────────────────────────────
# We don't want tests to actually call the Groq API
# because: it costs credits, it's slow, it needs internet
# So we "mock" it — replace the real API call with a
# fake one that returns a predictable response


MOCK_THREAT_MODEL = {
    "system_name": "Test Flask App",
    "overall_risk_score": 7,
    "trust_boundaries": [
        "Client to Flask API",
        "Flask API to PostgreSQL"
    ],
    "stride": {
        "spoofing": {
            "risk": "High",
            "threats": ["JWT token forgery"],
            "mitigations": ["Use RS256 algorithm"]
        },
        "tampering": {
            "risk": "Medium",
            "threats": ["SQL injection via unvalidated input"],
            "mitigations": ["Use parameterized queries"]
        },
        "repudiation": {
            "risk": "Low",
            "threats": ["No audit logging"],
            "mitigations": ["Implement structured logging"]
        },
        "information_disclosure": {
            "risk": "High",
            "threats": ["Sensitive data in logs"],
            "mitigations": ["Sanitize log output"]
        },
        "denial_of_service": {
            "risk": "Medium",
            "threats": ["No rate limiting on API"],
            "mitigations": ["Add rate limiting middleware"]
        },
        "elevation_of_privilege": {
            "risk": "Critical",
            "threats": ["Missing RBAC on admin endpoints"],
            "mitigations": ["Implement role-based access control"]
        }
    },
    "top_3_actions": [
        "Implement RBAC on all admin endpoints immediately",
        "Add rate limiting to prevent DoS attacks",
        "Rotate JWT secrets and switch to RS256"
    ]
}


# ─────────────────────────────────────────
# Test 1 — Output has correct structure
# ─────────────────────────────────────────

@patch("app.analyzer.Groq")
def test_threat_model_has_required_keys(mock_groq):
    """Generated threat model must have all required keys"""

    # Set up the mock to return our fake response
    mock_client = MagicMock()
    mock_groq.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = \
        '{"system_name": "Test", "overall_risk_score": 7, "trust_boundaries": [], ' \
        '"stride": {"spoofing": {"risk": "High", "threats": [], "mitigations": []}, ' \
        '"tampering": {"risk": "Low", "threats": [], "mitigations": []}, ' \
        '"repudiation": {"risk": "Low", "threats": [], "mitigations": []}, ' \
        '"information_disclosure": {"risk": "Low", "threats": [], "mitigations": []}, ' \
        '"denial_of_service": {"risk": "Low", "threats": [], "mitigations": []}, ' \
        '"elevation_of_privilege": {"risk": "Low", "threats": [], "mitigations": []}}, ' \
        '"top_3_actions": []}'

    parsed_input = {
        "content": "Flask app with JWT",
        "type": "raw",
        "source": "raw_input"
    }

    result = generate_threat_model(parsed_input)

    # Check all required top-level keys exist
    assert "system_name"        in result
    assert "overall_risk_score" in result
    assert "trust_boundaries"   in result
    assert "stride"             in result
    assert "top_3_actions"      in result


# ─────────────────────────────────────────
# Test 2 — STRIDE has all 6 categories
# ─────────────────────────────────────────

@patch("app.analyzer.Groq")
def test_stride_has_all_categories(mock_groq):
    """STRIDE section must contain all 6 categories"""

    import json
    mock_client = MagicMock()
    mock_groq.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = \
        json.dumps(MOCK_THREAT_MODEL)

    parsed_input = {
        "content": "Flask app with JWT",
        "type": "raw",
        "source": "raw_input"
    }

    result = generate_threat_model(parsed_input)

    stride = result["stride"]
    assert "spoofing"              in stride
    assert "tampering"             in stride
    assert "repudiation"           in stride
    assert "information_disclosure" in stride
    assert "denial_of_service"     in stride
    assert "elevation_of_privilege" in stride


# ─────────────────────────────────────────
# Test 3 — Risk score is a valid number
# ─────────────────────────────────────────

@patch("app.analyzer.Groq")
def test_risk_score_is_valid(mock_groq):
    """Overall risk score must be a number between 1 and 10"""

    import json
    mock_client = MagicMock()
    mock_groq.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = \
        json.dumps(MOCK_THREAT_MODEL)

    parsed_input = {
        "content": "Flask app with JWT",
        "type": "raw",
        "source": "raw_input"
    }

    result = generate_threat_model(parsed_input)

    score = result["overall_risk_score"]
    assert isinstance(score, (int, float))
    assert 1 <= score <= 10