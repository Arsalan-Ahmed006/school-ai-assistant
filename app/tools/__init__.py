"""app/tools/__init__.py

Public exports for the tools package.

Import all tools from here rather than from individual modules to maintain
a stable public API while keeping implementation details encapsulated.

Phase 2 addition:
    retrieve_knowledge — MCP-ready knowledge retrieval layer.
"""

from app.tools.classification import classify_request
from app.tools.formatting import format_lesson_plan, format_response
from app.tools.guardrails import check_guardrails, guardrail_callback
from app.tools.knowledge_retrieval import retrieve_knowledge
from app.tools.validation import validate_input

__all__ = [
    "validate_input",
    "classify_request",
    "format_response",
    "format_lesson_plan",
    "check_guardrails",
    "guardrail_callback",
    "retrieve_knowledge",
]
