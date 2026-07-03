# School AI Assistant — Engineering Context & Standards

> This file defines the engineering standards, conventions, and architecture decisions
> for the School AI Assistant project. All contributors (human and AI) must follow
> these rules when writing or reviewing code.
>
> **Scope:** Applies to all code under `app/`, `tests/`, and any future subagents.

---

## Project Identity

| Field | Value |
|-------|-------|
| **Project** | school-ai-assistant |
| **Framework** | Google ADK 2.0 (`google-adk>=2.0.0`) |
| **Model** | Gemini 2.5 Flash (`gemini-2.5-flash`) |
| **Runtime** | Python 3.11+ |
| **Auth** | Google AI Studio API key (local dev only) |
| **Session** | In-memory (no persistent storage) |
| **Deployment** | Local development — no cloud targets |

---

## Standard 1 — Python Type Hints

**Rule:** All functions, methods, and class attributes must carry full type annotations.
Type hints are not optional. They serve as inline documentation and enable static
analysis with `ty` (configured in `pyproject.toml`).

### ✅ Required Pattern

```python
from typing import Literal
from collections.abc import Sequence


def explain_concept(topic: str, grade_level: int) -> str:
    """Explain a school concept at the appropriate grade level."""
    ...


def search_curriculum(
    subject: str,
    keywords: Sequence[str],
    max_results: int = 5,
) -> list[dict[str, str]]:
    """Search curriculum resources for a subject."""
    ...


class LessonResult:
    topic: str
    summary: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    sources: list[str]
```

### ❌ Prohibited Pattern

```python
def explain_concept(topic, grade_level):  # No types — not allowed
    ...

def search_curriculum(subject, keywords):  # No return type — not allowed
    ...
```

### Rules
- Always annotate return types, including `-> None` for void functions.
- Use `str | None` (union syntax) over `Optional[str]` (Python 3.10+ style).
- Use `list[str]` over `List[str]` — prefer built-in generics.
- Import from `collections.abc` for abstract types (`Sequence`, `Mapping`, `Iterator`).

---

## Standard 2 — Pydantic Input Validation for All Tools

**Rule:** Every ADK tool that accepts structured or complex input must define a
Pydantic model for its input schema. Never trust raw string inputs for structured
data. Never parse user input with ad-hoc string splitting.

### Why This Matters
ADK tools are called by Gemini, which constructs arguments from natural language.
Pydantic ensures those arguments are valid before your logic runs, and produces
clear error messages when they are not.

### ✅ Required Pattern

```python
from pydantic import BaseModel, Field, field_validator


class GradeQuizInput(BaseModel):
    """Input schema for the grade_quiz tool."""

    student_answers: list[str] = Field(
        ...,
        min_length=1,
        description="List of student answer strings, one per question.",
    )
    correct_answers: list[str] = Field(
        ...,
        min_length=1,
        description="List of correct answer strings in the same order.",
    )
    subject: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="School subject being tested (e.g. 'Mathematics').",
    )

    @field_validator("correct_answers")
    @classmethod
    def answers_length_must_match(
        cls, v: list[str], info: ValidationInfo
    ) -> list[str]:
        student = info.data.get("student_answers", [])
        if len(v) != len(student):
            raise ValueError(
                f"correct_answers length ({len(v)}) must match "
                f"student_answers length ({len(student)})."
            )
        return v


def grade_quiz(input_data: GradeQuizInput) -> dict[str, int | str]:
    """Grade a student's quiz and return a score and feedback."""
    correct = sum(
        a.strip().lower() == b.strip().lower()
        for a, b in zip(input_data.student_answers, input_data.correct_answers)
    )
    total = len(input_data.correct_answers)
    return {
        "score": correct,
        "total": total,
        "percentage": round((correct / total) * 100),
        "subject": input_data.subject,
    }
```

### ❌ Prohibited Pattern

```python
def grade_quiz(student_answers: str, correct_answers: str) -> str:
    # Parsing comma-separated values from a string — fragile and unsafe
    student = student_answers.split(",")
    correct = correct_answers.split(",")
    ...
```

### Rules
- Define one Pydantic model per tool that has structured input.
- Use `Field(description=...)` — Gemini uses these descriptions to fill arguments correctly.
- Add `@field_validator` for cross-field validation rules.
- Return structured `dict` or Pydantic model outputs where possible.

---

## Standard 3 — No Hardcoded Secrets or API Keys

**Rule:** Zero secrets, credentials, API keys, passwords, or URLs containing tokens
may appear in source code, comments, or test files. All secrets are loaded from
environment variables at runtime.

### ✅ Required Pattern

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from app/.env automatically

def get_api_key(service_name: str) -> str:
    """Retrieve a required API key from the environment."""
    key = os.environ.get(f"{service_name.upper()}_API_KEY")
    if not key:
        raise EnvironmentError(
            f"Missing required environment variable: {service_name.upper()}_API_KEY. "
            f"Add it to app/.env and never commit that file."
        )
    return key
```

### ❌ Prohibited Pattern

```python
# NEVER do any of these:
API_KEY = "AIzaSyABC123..."                    # Hardcoded secret
GOOGLE_API_KEY = "AIzaSyABC123..."             # Hardcoded secret
url = "https://api.example.com?key=abc123"     # Secret in URL
password = "my_secret_password"               # Hardcoded credential
```

### Secret Locations
| Secret | Location | Committed to Git? |
|--------|----------|------------------|
| `GOOGLE_API_KEY` | `app/.env` | ❌ No — blocked by `.gitignore` |
| Any future API key | `app/.env` | ❌ No |
| Service account credentials | Environment variable | ❌ No |

### Rules
- Add new secrets to `app/.env` only. Never to `pyproject.toml`, `*.yaml`, or `*.py`.
- Reference secrets via `os.environ.get("VAR_NAME")`.
- Raise a clear `EnvironmentError` if a required secret is missing.
- Document required environment variables in `README.md`.

---

## Standard 4 — Modular and Reusable Agents

**Rule:** The project must be designed so that agents, tools, and subagents can be
composed and reused independently. No agent should be hard-coupled to a specific
caller or context.

### Architecture Pattern

```
app/
├── agent.py            # Root agent — composes sub-agents and core tools
├── agents/             # (future) One file per sub-agent
│   ├── tutor_agent.py      # Handles concept explanation and teaching
│   ├── quiz_agent.py       # Handles quiz generation and grading
│   └── research_agent.py   # Handles web search and resource lookup
├── tools/              # (future) One file per tool domain
│   ├── curriculum.py       # Tools: search_curriculum, get_lesson_plan
│   ├── assessment.py       # Tools: generate_quiz, grade_quiz
│   └── resources.py        # Tools: find_resource, summarize_document
└── app_utils/
    ├── telemetry.py
    └── typing.py
```

### ✅ Required Pattern — Sub-Agent Definition

```python
# app/agents/tutor_agent.py
from google.adk.agents import Agent
from google.adk.models import Gemini
from app.tools.curriculum import explain_concept, get_lesson_plan

# Each sub-agent is a self-contained module — importable anywhere
tutor_agent = Agent(
    name="tutor_agent",
    model=Gemini(model="gemini-2.5-flash"),
    description=(
        "Specializes in explaining academic concepts clearly "
        "and at the appropriate difficulty level."
    ),
    instruction=(
        "You are a patient and knowledgeable tutor. Explain concepts "
        "step-by-step, use examples, and check for understanding."
    ),
    tools=[explain_concept, get_lesson_plan],
)
```

```python
# app/agent.py — Root agent composes sub-agents
from google.adk.agents import Agent
from app.agents.tutor_agent import tutor_agent
from app.agents.quiz_agent import quiz_agent

root_agent = Agent(
    name="school_ai_assistant",
    ...
    sub_agents=[tutor_agent, quiz_agent],  # Delegation via sub-agents
)
```

### Rules
- One sub-agent per file under `app/agents/`.
- One tool domain per file under `app/tools/`.
- Sub-agents must be importable without side effects.
- The root agent in `agent.py` is the only composition point.
- Never import one sub-agent from inside another sub-agent.

---

## Standard 5 — Small, Focused Tools

**Rule:** Each tool function must do exactly one thing and do it well. If you find
yourself writing `and` in a tool's docstring, the tool should be split in two.

### The Single Responsibility Rule for Tools
A tool should: accept a focused input, perform one operation, return a clear output.

### ✅ Required Pattern — Focused Tools

```python
# app/tools/curriculum.py

def get_topic_summary(topic: str) -> str:
    """Return a one-paragraph summary of a school curriculum topic.

    Args:
        topic: The curriculum topic name (e.g. 'Photosynthesis', 'Algebra').

    Returns:
        A concise summary suitable for a student introduction.
    """
    ...


def get_related_topics(topic: str, subject: str) -> list[str]:
    """Return a list of topics related to the given topic within a subject.

    Args:
        topic: The starting topic name.
        subject: The school subject (e.g. 'Biology', 'Mathematics').

    Returns:
        A list of related topic names (up to 5).
    """
    ...


def get_difficulty_level(topic: str, grade: int) -> str:
    """Assess whether a topic is appropriate for a given grade level.

    Args:
        topic: The curriculum topic name.
        grade: The student's grade level (1–12).

    Returns:
        One of: 'too easy', 'appropriate', 'too advanced'.
    """
    ...
```

### ❌ Prohibited Pattern — Monolithic Tool

```python
def handle_curriculum_request(
    topic: str, grade: int, subject: str, include_summary: bool,
    include_related: bool, check_difficulty: bool, ...
) -> dict:
    # Does too many things — impossible for Gemini to call correctly
    # and impossible to test in isolation
    ...
```

### Tool Docstring Requirements
Every tool docstring must include:
1. **One-sentence description** — what it does (Gemini reads this to decide when to call it)
2. **`Args:` section** — each parameter explained
3. **`Returns:` section** — exact format of the return value

---

## Standard 6 — Graceful Error Handling

**Rule:** Tools must never raise unhandled exceptions to the agent. All errors must
be caught, logged, and returned as descriptive error strings or structured error
objects. Gemini will read the error string and explain it to the user helpfully.

### ✅ Required Pattern

```python
import logging

logger = logging.getLogger(__name__)


def search_curriculum(query: str, subject: str) -> str | dict:
    """Search curriculum database for resources.

    Args:
        query: The search query string.
        subject: The school subject to search within.

    Returns:
        A JSON-serializable dict of results, or an error string.
    """
    # Validate inputs before processing
    if not query.strip():
        return "Error: search query cannot be empty."
    if len(query) > 500:
        return "Error: search query is too long (max 500 characters)."

    try:
        results = _call_curriculum_api(query=query, subject=subject)
        return {"results": results, "count": len(results)}

    except TimeoutError:
        logger.warning("Curriculum API timed out for query: %s", query)
        return (
            "The curriculum search service is temporarily unavailable. "
            "Please try again in a moment."
        )
    except ValueError as e:
        logger.error("Invalid curriculum query: %s | error: %s", query, e)
        return f"Invalid search parameters: {e}"
    except Exception as e:
        # Catch-all: log the full traceback, return a safe message
        logger.exception("Unexpected error in search_curriculum: %s", e)
        return (
            "An unexpected error occurred while searching curriculum. "
            "The issue has been logged."
        )
```

### ❌ Prohibited Pattern

```python
def search_curriculum(query: str) -> dict:
    # No error handling — an exception here crashes the entire agent turn
    results = _call_curriculum_api(query)
    return results
```

### Rules
- Validate inputs at the top of every tool before doing any work.
- Use `try/except` for all I/O operations (API calls, file reads, network requests).
- Catch specific exceptions first, then a broad `Exception` last.
- Always `logger.exception()` for unexpected errors (captures the full traceback).
- Return descriptive human-readable strings for errors — Gemini will relay them.
- Never `raise` from a tool function unless it is a programming error, not a runtime error.

---

## Standard 7 — Log Important Workflow Events

**Rule:** All significant workflow events — agent decisions, tool calls, errors,
and state changes — must be logged at the appropriate severity level using Python's
standard `logging` module.

### Logger Setup

```python
# At the top of every module that logs:
import logging

# Use the module's __name__ — produces scoped log output like:
# app.tools.curriculum — INFO — Searching curriculum for: 'Photosynthesis'
logger = logging.getLogger(__name__)
```

### Log Level Guide

| Level | When to Use | Example |
|-------|-------------|---------|
| `logger.debug()` | Detailed internal state (disabled in prod) | Raw API response payloads |
| `logger.info()` | Normal workflow milestones | "Tool called: explain_concept, topic=Algebra" |
| `logger.warning()` | Recoverable issues | "Curriculum API slow, retrying..." |
| `logger.error()` | Handled failures | "Quiz grading failed: mismatched answer lengths" |
| `logger.exception()` | Unexpected errors (includes traceback) | Inside `except Exception as e:` blocks |

### ✅ Required Pattern

```python
def explain_concept(topic: str, grade_level: int) -> str:
    """Explain a school concept at the appropriate grade level."""
    logger.info(
        "explain_concept called | topic=%s | grade_level=%d", topic, grade_level
    )

    if grade_level < 1 or grade_level > 12:
        logger.warning(
            "Invalid grade_level=%d for topic=%s, clamping to range [1, 12]",
            grade_level, topic,
        )
        grade_level = max(1, min(12, grade_level))

    try:
        result = _generate_explanation(topic, grade_level)
        logger.debug("explain_concept result length: %d chars", len(result))
        return result
    except Exception as e:
        logger.exception("Failed to explain concept: %s | error: %s", topic, e)
        return f"Sorry, I could not generate an explanation for '{topic}'."
```

### Rules
- Use `%s` style formatting in log calls, not f-strings (deferred evaluation is faster).
- Never log raw secrets, API keys, or personally identifiable information (PII).
- Use `logger.info()` at the entry point of every tool call.
- Use `logger.exception()` (not `logger.error()`) inside `except` blocks to capture tracebacks.

---

## Standard 8 — Secure Coding Practices

**Rule:** The codebase must follow OWASP secure coding principles adapted for
AI agent development. Security is not an afterthought.

### 8.1 Input Sanitization

```python
import html
import re

# Strip and sanitize user-facing inputs before processing
def sanitize_student_input(raw: str) -> str:
    """Remove control characters and HTML from student input."""
    stripped = raw.strip()
    # Remove HTML tags
    no_html = html.escape(stripped)
    # Remove non-printable control characters (except newline/tab)
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", no_html)
    return sanitized
```

### 8.2 No Prompt Injection

```python
# ❌ NEVER interpolate raw user input directly into agent instructions
root_agent = Agent(
    instruction=f"Help this student: {user_input}"  # Prompt injection risk
)

# ✅ Pass user content through the message channel only — never into instruction=
message = types.Content(
    role="user",
    parts=[types.Part.from_text(text=sanitize_student_input(user_input))]
)
```

### 8.3 Path Traversal Prevention

```python
import os
from pathlib import Path

ALLOWED_DOCS_DIR = Path("app/resources").resolve()

def read_resource_file(filename: str) -> str:
    """Safely read a resource file within the allowed directory."""
    # Resolve to absolute path and verify it is inside the allowed directory
    target = (ALLOWED_DOCS_DIR / filename).resolve()
    if not str(target).startswith(str(ALLOWED_DOCS_DIR)):
        raise PermissionError(f"Access denied: path traversal detected for '{filename}'.")
    return target.read_text(encoding="utf-8")
```

### 8.4 Rate Limiting Awareness

```python
# Add exponential backoff for external API calls
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def _call_external_api(query: str) -> dict:
    """Call an external API with automatic retry and backoff."""
    ...
```

### Security Checklist (verify before any PR)
- [ ] No secrets in source files
- [ ] All user inputs validated with Pydantic or explicit checks
- [ ] No raw user input interpolated into prompts or instructions
- [ ] File paths validated against allowed directories
- [ ] External API calls use retry/backoff
- [ ] No debug endpoints exposed in production mode
- [ ] Logging does not emit PII or sensitive data

---

## Standard 9 — Clear Comments Explaining Decisions

**Rule:** Comments must explain **why** a decision was made, not **what** the code does.
The code itself shows what happens. Comments show the intent, the tradeoff, or the constraint.

### ✅ Required Pattern — Decision Comments

```python
# We use in-memory session storage here instead of a database because
# this project is local-dev-only. When persistence is needed, swap
# session_service_uri=None for a Cloud SQL URI — no other changes required.
session_service_uri = None


# Grade level is clamped to [1, 12] rather than raising an error because
# Gemini may sometimes infer a grade from context (e.g. "college" → 13).
# Clamping keeps the agent flowing instead of breaking mid-conversation.
grade_level = max(1, min(12, grade_level))


# The docstring is intentionally detailed here. ADK passes this docstring
# verbatim to Gemini so it knows when and how to call this tool.
# A vague docstring leads to Gemini calling the tool incorrectly.
def explain_concept(topic: str, grade_level: int) -> str:
    """Explain a school curriculum concept using age-appropriate language.
    ...
    """
```

### ❌ Prohibited Pattern — Noise Comments

```python
# Set grade_level to the max of 1 and the min of 12 and grade_level
grade_level = max(1, min(12, grade_level))   # restates the code — useless

# Import logging
import logging                               # obvious — useless

x = x + 1  # Increment x                   # obvious — useless
```

### Comment Standards
- Write a module-level docstring in every new file explaining its purpose.
- Write function docstrings for all public functions (required by ADK for tools).
- Use inline `#` comments only when explaining a non-obvious decision or constraint.
- Reference the relevant ADK documentation or GitHub issue when working around a framework bug.
- Keep comments up to date — a wrong comment is worse than no comment.

---

## Standard 10 — Maintainability and Readability

**Rule:** Code is read far more often than it is written. Every design choice must
optimize for the next developer (or AI assistant) reading the code, not for the
convenience of the current author.

### 10.1 Naming Conventions

```python
# Modules — lowercase_with_underscores
# app/tools/curriculum_search.py

# Classes — PascalCase
class CurriculumSearchResult:
    ...

# Functions and variables — lowercase_with_underscores
def search_curriculum(query: str) -> list[CurriculumSearchResult]:
    ...

# Constants — UPPERCASE_WITH_UNDERSCORES
MAX_SEARCH_RESULTS: int = 10
DEFAULT_GRADE_LEVEL: int = 8

# ADK Agent objects — descriptive snake_case ending in _agent
tutor_agent = Agent(...)
quiz_agent = Agent(...)
root_agent = Agent(...)  # Always root_agent for the top-level agent
```

### 10.2 Function Length

- **Tool functions:** Maximum 40 lines. If longer, extract a private helper (`_helper_name`).
- **Private helpers:** Maximum 60 lines.
- **Classes:** Maximum 150 lines. Larger classes should be split into modules.

### 10.3 File Organization

Every file under `app/` must follow this structure:

```python
# 1. Standard library imports
import os
import logging
from typing import Literal

# 2. Third-party imports
from pydantic import BaseModel, Field
from google.adk.agents import Agent

# 3. Local imports
from app.tools.curriculum import explain_concept

# 4. Module-level constants
logger = logging.getLogger(__name__)
MAX_RESULTS: int = 10

# 5. Pydantic models (for this module's tools)
class SearchInput(BaseModel):
    ...

# 6. Private helper functions (prefixed with _)
def _call_api(query: str) -> dict:
    ...

# 7. Public tool functions
def search_curriculum(input_data: SearchInput) -> list[dict]:
    ...

# 8. Agent definitions (only in agent.py and agents/*.py)
tutor_agent = Agent(...)
```

### 10.4 No Magic Numbers

```python
# ❌ Magic numbers — unreadable and unmaintainable
if grade_level > 12:
    ...
results = results[:10]

# ✅ Named constants — self-documenting
MAX_GRADE_LEVEL: int = 12
MAX_SEARCH_RESULTS: int = 10

if grade_level > MAX_GRADE_LEVEL:
    ...
results = results[:MAX_SEARCH_RESULTS]
```

### 10.5 Avoid Abbreviations

```python
# ❌ Abbreviated — unclear
def get_q(subj: str, lvl: int, n: int) -> list:
    ...

# ✅ Full names — readable
def generate_quiz_questions(
    subject: str,
    difficulty_level: int,
    question_count: int,
) -> list[str]:
    ...
```

---

## Enforcement

These standards are enforced through:

| Tool | What It Checks | Command |
|------|---------------|---------|
| `ruff` | Style, imports, common bugs | `agents-cli lint` |
| `ty` | Type annotation correctness | `uv run ty check app/` |
| `pytest` | Functional correctness | `uv run pytest tests/unit tests/integration` |
| `agents-cli eval` | Response quality (1–5 score) | `agents-cli eval generate && agents-cli eval grade` |

All four must pass before any feature is considered complete.

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-06-29 | Initial engineering standards established | Arsalan-Ahmed006 |
