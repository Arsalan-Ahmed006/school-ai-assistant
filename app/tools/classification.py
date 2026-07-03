"""app/tools/classification.py

Lightweight rule-based classification tool for School AI Assistant.

Helps sub-agents and tools to helper-verify or fallback-check that queries
are routed to the correct domain, distinguishing between parent FAQs,
teacher lesson planning, or unsupported queries.
"""

from app.app_utils.logging_config import get_logger

logger = get_logger(__name__)

# Topic keywords
PARENT_KEYWORDS = [
    "fees",
    "schedule",
    "policy",
    "holiday",
    "admission",
    "uniform",
    "report card",
    "fee",
    "term",
    "calendar",
    "enrollment",
    "tuition",
]
TEACHER_KEYWORDS = [
    "lesson",
    "plan",
    "activity",
    "assessment",
    "strategy",
    "objective",
    "curriculum",
    "teach",
    "classroom",
    "worksheet",
    "quiz",
    "grade level",
    "pedagogical",
    "rubric",
]


def classify_request(message: str, role: str = "unknown") -> dict:
    """Classify a school-related request into parent_faq, lesson_plan, or unsupported.

    This is a helper tool for validation/guardrails, not the primary ADK router.

    Args:
        message: Sanitized user message.
        role: Declared user role ("parent", "teacher", "unknown").

    Returns:
        dict: Keys are:
            - 'category' (str): "parent_faq", "lesson_plan", or "unsupported".
            - 'confidence' (str): "high", "medium", or "low".
            - 'role_hint' (str): The inferred or given role.
    """
    logger.info("event=classification_started | role=%s", role)

    msg_lower = message.lower()
    parent_matches = sum(1 for kw in PARENT_KEYWORDS if kw in msg_lower)
    teacher_matches = sum(1 for kw in TEACHER_KEYWORDS if kw in msg_lower)

    role_clean = role.strip().lower()

    # Determine category and confidence based on keywords and role
    if parent_matches > 0 and teacher_matches == 0:
        category = "parent_faq"
        confidence = "high" if role_clean == "parent" else "medium"
    elif teacher_matches > 0 and parent_matches == 0:
        category = "lesson_plan"
        confidence = "high" if role_clean == "teacher" else "medium"
    elif parent_matches > 0 and teacher_matches > 0:
        # Conflicting keywords
        if role_clean == "parent":
            category = "parent_faq"
            confidence = "medium"
        elif role_clean == "teacher":
            category = "lesson_plan"
            confidence = "medium"
        else:
            category = "unsupported"
            confidence = "low"
    else:
        # No keywords matched
        if role_clean == "parent":
            category = "parent_faq"
            confidence = "low"
        elif role_clean == "teacher":
            category = "lesson_plan"
            confidence = "low"
        else:
            category = "unsupported"
            confidence = "high"

    logger.info(
        "event=classification_completed | category=%s | confidence=%s",
        category,
        confidence,
    )
    return {
        "category": category,
        "confidence": confidence,
        "role_hint": role_clean,
    }
