"""tests/unit/test_formatting.py

Unit tests for app/tools/formatting.py.

All tests are pure Python — no ADK objects, no Gemini API calls.
"""

import pytest
from app.tools.formatting import format_response, format_lesson_plan


# ──────────────────────── format_response ──────────────────────────────────

def test_format_response_contains_content():
    result = format_response("Here are the school fees.", role="parent")
    assert result["content"] == "Here are the school fees."


def test_format_response_includes_timestamp():
    result = format_response("Some answer", role="teacher")
    assert "formatted_at" in result
    # Must be a non-empty ISO string
    assert len(result["formatted_at"]) > 0


def test_format_response_word_count():
    result = format_response("Hello world this is four", role="parent")
    assert result["word_count"] == 5


def test_format_response_normalises_role():
    result = format_response("Something", role="  PARENT  ")
    assert result["role"] == "parent"


def test_format_response_unknown_role():
    result = format_response("Something", role="unknown")
    assert result["role"] == "unknown"


# ──────────────────────── format_lesson_plan ───────────────────────────────

def test_format_lesson_plan_has_all_six_sections():
    result = format_lesson_plan("Photosynthesis", grade_level=6, subject="Science")
    sections = result["sections"]
    assert "learning_objectives" in sections
    assert "materials" in sections
    assert "teaching_activities" in sections
    assert "assessment" in sections
    assert "homework" in sections
    assert "time_allocation" in sections


def test_format_lesson_plan_time_allocation_sums_to_duration():
    duration = 60
    result = format_lesson_plan("Fractions", grade_level=5, duration_minutes=duration)
    alloc = result["sections"]["time_allocation"]
    # Extract integer minutes from each string value e.g. "5 minutes" → 5
    total = sum(int(v.split()[0]) for v in alloc.values())
    assert total == duration


def test_format_lesson_plan_default_duration():
    result = format_lesson_plan("Fractions", grade_level=4)
    assert result["duration_minutes"] == 45
    alloc = result["sections"]["time_allocation"]
    total = sum(int(v.split()[0]) for v in alloc.values())
    assert total == 45


def test_format_lesson_plan_rejects_invalid_grade_above_12():
    result = format_lesson_plan("History", grade_level=15)
    # Should clamp to 12
    assert result["grade_level"] == 12


def test_format_lesson_plan_rejects_invalid_grade_below_1():
    result = format_lesson_plan("History", grade_level=0)
    # Should clamp to 1
    assert result["grade_level"] == 1


def test_format_lesson_plan_contains_topic_and_subject():
    result = format_lesson_plan("The Water Cycle", grade_level=3, subject="Geography")
    assert result["topic"] == "The Water Cycle"
    assert result["subject"] == "Geography"


def test_format_lesson_plan_default_subject():
    result = format_lesson_plan("Algebra", grade_level=8)
    assert result["subject"] == "General"
