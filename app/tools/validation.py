"""app/tools/validation.py

Input validation and sanitisation tools for the School AI Assistant.

Ensures that all incoming messages are cleaned, HTML is escaped to prevent injection,
control characters are removed, and length limits are respected before being
processed by the agents.
"""

import html
import re
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from app.app_utils.logging_config import get_logger

logger = get_logger(__name__)

# Constants
MAX_MESSAGE_LENGTH = 2000
CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class UserRole(str, Enum):
    """Supported roles for users interacting with the school assistant."""

    PARENT = "parent"
    TEACHER = "teacher"
    UNKNOWN = "unknown"


class IncomingRequest(BaseModel):
    """Pydantic model representing a structured user request."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=MAX_MESSAGE_LENGTH,
        description="The user's query or instruction.",
    )
    role: UserRole = Field(
        default=UserRole.UNKNOWN,
        description="The declared or inferred role of the user.",
    )


class ValidationResult(BaseModel):
    """Pydantic model representing the output of the validation tool."""

    valid: bool = Field(
        ..., description="True if the request is valid and safe to process."
    )
    sanitized_message: str = Field(
        ..., description="The sanitized request string."
    )
    role: UserRole = Field(..., description="The validated role of the user.")
    error: str | None = Field(
        default=None, description="Details about the validation failure if any."
    )


def validate_input(message: str, role: str = "unknown") -> dict:
    """Validate and sanitise user input before processing.

    Strips control characters, escapes HTML tags, enforces character limits,
    and returns a structured validation dict.

    Args:
        message: The raw user message string.
        role: The user role string (e.g. parent, teacher).

    Returns:
        dict: Matching the ValidationResult schema.
    """
    logger.info("event=validation_started | role=%s | msg_len=%d", role, len(message))

    # Strip whitespace first
    raw_message = message.strip()

    # Pre-validation for role matching Enum
    role_enum = UserRole.UNKNOWN
    try:
        cleaned_role = role.strip().lower()
        if cleaned_role in (UserRole.PARENT.value, UserRole.TEACHER.value):
            role_enum = UserRole(cleaned_role)
    except Exception:
        pass

    # Validate using Pydantic
    try:
        # Enforce basic constraints via model instantiation
        IncomingRequest(message=raw_message, role=role_enum)
    except ValidationError as e:
        error_msg = e.errors()[0]["msg"]
        logger.warning(
            "event=validation_failure | reason=pydantic_validation_error | error=%s",
            error_msg,
        )
        return {
            "valid": False,
            "sanitized_message": "",
            "role": role_enum,
            "error": f"Validation failed: {error_msg}",
        }

    # Escaping HTML tags to prevent cross-site scripting/injection patterns
    escaped = html.escape(raw_message)

    # Stripping non-printable control characters
    sanitized = CONTROL_CHAR_PATTERN.sub("", escaped)

    # Double check it is not empty after sanitisation
    if not sanitized:
        logger.warning("event=validation_failure | reason=empty_after_sanitization")
        return {
            "valid": False,
            "sanitized_message": "",
            "role": role_enum,
            "error": "Validation failed: message is empty after sanitization.",
        }

    logger.info("event=validation_success | role=%s", role_enum.value)
    return {
        "valid": True,
        "sanitized_message": sanitized,
        "role": role_enum,
        "error": None,
    }
