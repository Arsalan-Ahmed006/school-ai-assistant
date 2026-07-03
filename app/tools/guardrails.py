"""app/tools/guardrails.py

Security guardrails for the School AI Assistant.

Inspects incoming user messages for potential prompt injection, jailbreak attempts,
secret prompt extraction, and offensive keywords before they are processed by
any agent.
"""

import re
from typing import Literal
from google.genai import types
from google.adk.agents.callback_context import CallbackContext

from app.app_utils.config import get_config
from app.app_utils.logging_config import get_logger

logger = get_logger(__name__)

# Threat detection compiled patterns
PROMPT_INJECTION_PATTERN = re.compile(
    r"(ignore\s+previous|ignore\s+your\s+instructions|override\s+system|disregard|new\s+instructions:)",
    re.IGNORECASE,
)
JAILBREAK_PATTERN = re.compile(
    r"(\bdan\b|act\s+as\s+a|pretend\s+you\s+are|you\s+are\s+now|developer\s+mode|jailbreak|bypass)",
    re.IGNORECASE,
)
SECRET_EXTRACTION_PATTERN = re.compile(
    r"(show\s+me\s+your\s+prompt|reveal\s+your\s+instructions|what\s+is\s+your\s+system\s+prompt|api\s+key|secret\s+key|your\s+instructions\s+are)",
    re.IGNORECASE,
)


class GuardrailResult:
    """Represents the results of checking a message against safety rules."""

    def __init__(
        self,
        safe: bool,
        threat_category: Literal[
            "prompt_injection",
            "jailbreak",
            "secret_extraction",
            "offensive_content",
            "safe",
        ] = "safe",
        reason: str | None = None,
    ) -> None:
        self.safe = safe
        self.threat_category = threat_category
        self.reason = reason


def check_guardrails(message: str) -> GuardrailResult:
    """Analyze a user message to detect prompt injection, jailbreaks, or policy violations.

    Args:
        message: The raw or sanitized message string.

    Returns:
        GuardrailResult: Safety outcome and matched threat category.
    """
    # 1. Prompt Injection Check
    if PROMPT_INJECTION_PATTERN.search(message):
        return GuardrailResult(
            safe=False,
            threat_category="prompt_injection",
            reason="Potential prompt injection detected.",
        )

    # 2. Jailbreak Check
    if JAILBREAK_PATTERN.search(message):
        return GuardrailResult(
            safe=False,
            threat_category="jailbreak",
            reason="Potential jailbreak attempt detected.",
        )

    # 3. Secret Extraction Check
    if SECRET_EXTRACTION_PATTERN.search(message):
        return GuardrailResult(
            safe=False,
            threat_category="secret_extraction",
            reason="System prompt or API key extraction attempt detected.",
        )

    # 4. Offensive Keywords Check
    config = get_config()
    if config.offensive_keywords:
        lower_message = message.lower()
        for kw in config.offensive_keywords:
            if kw and kw in lower_message:
                return GuardrailResult(
                    safe=False,
                    threat_category="offensive_content",
                    reason=f"Offensive content keyword matched: '{kw}'.",
                )

    return GuardrailResult(safe=True)


def guardrail_callback(callback_context: CallbackContext) -> types.Content | None:
    """ADK hook executed before the root agent runs to filter out unsafe input.

    Logs request_received and guardrail_decision events. If unsafe, returns
    a Content object refusing the request, stopping execution.

    Args:
        callback_context: CallbackContext containing current session and user content.

    Returns:
        types.Content | None: Polite refusal Content if unsafe, None otherwise.
    """
    user_content = callback_context.user_content
    user_message = ""
    if user_content and user_content.parts:
        text_parts = [p.text for p in user_content.parts if p.text]
        user_message = " ".join(text_parts)

    # Log request_received event (truncating message to protect PII)
    logger.info("event=request_received | message_length=%d", len(user_message))

    # Evaluate safety
    result = check_guardrails(user_message)

    # Log guardrail_decision event
    logger.info(
        "event=guardrail_decision | safe=%s | category=%s | reason=%s",
        result.safe,
        result.threat_category,
        result.reason,
    )

    if not result.safe:
        return types.Content(
            role="model",
            parts=[
                types.Part(
                    text="I cannot fulfill this request as it violates ABC School's safety policies."
                )
            ],
        )

    return None
