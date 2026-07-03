"""tests/unit/test_classification.py

Unit tests for app/tools/classification.py.

All tests are pure Python — no ADK objects, no Gemini API calls.
"""

import pytest
from app.tools.classification import classify_request


def test_classifies_parent_fee_query():
    result = classify_request("What are the school fees?", role="parent")
    assert result["category"] == "parent_faq"


def test_classifies_parent_schedule_query():
    result = classify_request("What is the term schedule?", role="parent")
    assert result["category"] == "parent_faq"


def test_classifies_parent_holiday_query():
    result = classify_request("When is the next holiday?", role="unknown")
    assert result["category"] == "parent_faq"


def test_classifies_teacher_lesson_plan():
    result = classify_request("Create a lesson plan for photosynthesis", role="teacher")
    assert result["category"] == "lesson_plan"


def test_classifies_teacher_assessment():
    result = classify_request("Design an assessment for Grade 7 students", role="teacher")
    assert result["category"] == "lesson_plan"


def test_classifies_unsupported_weather():
    result = classify_request("What is the weather like today?", role="unknown")
    assert result["category"] == "unsupported"


def test_role_hint_influences_confidence_parent():
    result = classify_request("Tell me about fees", role="parent")
    assert result["confidence"] == "high"
    assert result["role_hint"] == "parent"


def test_role_hint_influences_confidence_teacher():
    result = classify_request("I need a lesson plan", role="teacher")
    assert result["confidence"] == "high"
    assert result["role_hint"] == "teacher"


def test_role_hint_unknown_lowers_confidence():
    result = classify_request("I need a lesson plan", role="unknown")
    assert result["confidence"] == "medium"


def test_result_contains_all_keys():
    result = classify_request("What are the fees?")
    assert "category" in result
    assert "confidence" in result
    assert "role_hint" in result
