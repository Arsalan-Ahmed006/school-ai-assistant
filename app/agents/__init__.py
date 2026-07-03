"""app/agents/__init__.py

Public exports for the agents package.

Import agents from here, not from individual files, to maintain a
stable public API while keeping implementation details encapsulated.
"""

from app.agents.parent_faq_agent import parent_faq_agent
from app.agents.teacher_lesson_agent import teacher_lesson_agent

__all__ = ["parent_faq_agent", "teacher_lesson_agent"]
