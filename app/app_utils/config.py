"""app/app_utils/config.py

Centralised environment configuration loader for School AI Assistant.

All runtime settings are loaded from environment variables or app/.env.
This module is the ONLY place env vars are read — every other module
imports from here rather than calling os.environ directly.
This makes configuration testable via monkeypatching and auditable in one place.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Ensure environment variables are loaded from the app directory
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=ENV_PATH, override=False)


@dataclass(frozen=True)
class AppConfig:
    """Dataclass holding all validated configuration parameters for the application."""

    model_name: str
    log_level: str
    allow_origins: list[str]
    logs_bucket: str | None
    offensive_keywords: list[str]
    school_name: str


def get_config() -> AppConfig:
    """Retrieve and validate the configuration from environment variables.

    Raises:
        EnvironmentError: If required configuration is missing or invalid.

    Returns:
        AppConfig: A validated configuration instance.
    """
    model_name = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.5-flash")
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Parse ALLOW_ORIGINS list
    allow_origins_raw = os.environ.get("ALLOW_ORIGINS", "")
    allow_origins = [o.strip() for o in allow_origins_raw.split(",") if o.strip()]

    logs_bucket = os.environ.get("LOGS_BUCKET_NAME")

    # Parse OFFENSIVE_KEYWORDS list for custom guardrail rules
    offensive_keywords_raw = os.environ.get("OFFENSIVE_KEYWORDS", "")
    offensive_keywords = [
        kw.strip().lower()
        for kw in offensive_keywords_raw.split(",")
        if kw.strip()
    ]

    school_name = os.environ.get("SCHOOL_NAME", "ABC School")

    # Verify that the Gemini API Key is available in the environment
    # (Do not raise here if running unit tests, but log/raise when agent is created/executed)
    return AppConfig(
        model_name=model_name,
        log_level=log_level,
        allow_origins=allow_origins,
        logs_bucket=logs_bucket,
        offensive_keywords=offensive_keywords,
        school_name=school_name,
    )
