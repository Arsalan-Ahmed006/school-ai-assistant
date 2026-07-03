"""tests/unit/test_validation.py

Unit tests for app/tools/validation.py.

All tests are pure Python — no ADK objects, no Gemini API calls.
"""

import pytest
from app.tools.validation import validate_input


def test_validate_accepts_valid_parent_query():
    result = validate_input("What are the school fees?", role="parent")
    assert result["valid"] is True
    assert result["role"] == "parent"
    assert result["error"] is None


def test_validate_accepts_valid_teacher_query():
    result = validate_input("Create a lesson plan for Grade 5 fractions", role="teacher")
    assert result["valid"] is True
    assert result["role"] == "teacher"


def test_validate_strips_html():
    result = validate_input("<script>alert('xss')</script>What are the fees?", role="parent")
    assert result["valid"] is True
    assert "<script>" not in result["sanitized_message"]


def test_validate_rejects_empty_string():
    result = validate_input("   ", role="unknown")
    assert result["valid"] is False
    assert result["error"] is not None


def test_validate_rejects_too_long_message():
    long_msg = "A" * 2001
    result = validate_input(long_msg, role="parent")
    assert result["valid"] is False
    assert result["error"] is not None


def test_validate_rejects_control_characters():
    msg = "Hello\x00World\x07"
    result = validate_input(msg, role="unknown")
    assert result["valid"] is True
    assert "\x00" not in result["sanitized_message"]
    assert "\x07" not in result["sanitized_message"]


def test_validate_known_roles():
    for role in ["parent", "teacher", "unknown"]:
        result = validate_input("What is the schedule?", role=role)
        assert result["valid"] is True
        assert result["role"] == role


def test_validate_unknown_role_defaults():
    result = validate_input("Some question", role="admin")
    assert result["valid"] is True
    assert result["role"] == "unknown"
