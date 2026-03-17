import pytest
from app.parser import parse_input


# ─────────────────────────────────────────
# Test 1 — Valid markdown file
# ─────────────────────────────────────────

def test_parse_markdown_file():
    """README.md should be detected as markdown type"""
    result = parse_input("README.md")

    # Check all 3 keys exist
    assert "content"  in result
    assert "type"     in result
    assert "source"   in result

    # Check values are correct
    assert result["type"]   == "markdown"
    assert result["source"] == "README.md"

    # Check content is not empty
    assert len(result["content"]) > 0


# ─────────────────────────────────────────
# Test 2 — Raw text input
# ─────────────────────────────────────────

def test_parse_raw_text():
    """A plain string should be treated as raw input"""
    result = parse_input("Flask app with JWT auth and PostgreSQL")

    assert result["type"]    == "text"
    assert result["source"]  == "raw_input"
    assert result["content"] == "Flask app with JWT auth and PostgreSQL"


# ─────────────────────────────────────────
# Test 3 — Non-existent file treated as raw text
# ─────────────────────────────────────────

def test_parse_nonexistent_file_as_raw():
    """A filename that doesn't exist should be treated as raw text"""
    result = parse_input("nonexistent_file.md")

    # Since file doesn't exist, should fall back to raw
    assert result["type"]   == "text`"
    assert result["source"] == "raw_input"


# ─────────────────────────────────────────
# Test 4 — .txt file detection
# ─────────────────────────────────────────

def test_parse_txt_file():
    """A .txt file should be detected as text type"""

    # Create a temporary .txt file for testing
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8"
    ) as f:
        f.write("This is a test architecture description")
        temp_path = f.name

    try:
        result = parse_input(temp_path)
        assert result["type"]    == "text"
        assert result["content"] == "This is a test architecture description"
    finally:
        os.unlink(temp_path)  # always clean up temp file


# ─────────────────────────────────────────
# Test 5 — Empty string input
# ─────────────────────────────────────────

def test_parse_empty_string():
    """Empty string should still return a valid dict"""
    result = parse_input("")

    assert "content" in result
    assert "type"    in result
    assert "source"  in result

