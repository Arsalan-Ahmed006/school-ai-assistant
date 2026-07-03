"""
Root conftest.py — shared pytest fixtures and configuration.

This file is auto-loaded by pytest before any test module runs.
Add fixtures here that need to be available across unit, integration,
and eval test suites. Test-suite-specific fixtures belong in the
conftest.py inside that suite's directory (e.g., tests/unit/conftest.py).
"""

import logging
import os

import pytest

# ---------------------------------------------------------------------------
# Logging setup for test runs
# ---------------------------------------------------------------------------
# Pytest captures log output by default; this logger is used in fixtures below.
# Test output at WARNING+ is shown on failure; set LOG_LEVEL=DEBUG to see more.
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Environment / secrets fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def require_env_vars() -> None:
    """Warn (not fail) if GOOGLE_API_KEY is absent during the test session.

    We warn rather than fail because unit tests must be runnable without
    a live API key. Integration tests that actually call Gemini should
    skip themselves using pytest.importorskip or a custom mark if the key
    is missing — not rely on this fixture to enforce it.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        logger.warning(
            "GOOGLE_API_KEY is not set. "
            "Integration tests that call Gemini will be skipped or fail. "
            "Add GOOGLE_API_KEY to app/.env to run the full test suite."
        )


# ---------------------------------------------------------------------------
# Async event-loop fixture (pytest-asyncio)
# ---------------------------------------------------------------------------
# asyncio_mode = "auto" is set in pyproject.toml, so async test functions
# are discovered automatically without @pytest.mark.asyncio decorators.
# The fixture below is kept for documentation purposes — pytest-asyncio
# creates its own loop fixture when asyncio_mode="auto".


# ---------------------------------------------------------------------------
# Shared data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_student_profile() -> dict[str, str | int]:
    """Return a minimal student profile dict for use in tool tests.

    Yields a fresh dict on each test so mutations in one test
    do not bleed into another.
    """
    return {
        "name": "Test Student",
        "grade_level": 8,
        "subject": "Mathematics",
    }


@pytest.fixture
def sample_curriculum_topic() -> str:
    """Return a stable topic string for curriculum tool tests."""
    return "Photosynthesis"
