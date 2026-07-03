# School AI Assistant — Architecture

## Overview

School AI Assistant is a conversational AI agent built on **Google ADK 2.0** using **Gemini 2.5 Flash**. It is designed exclusively for local development and educational use.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| AI Framework | Google ADK 2.0 (`google-adk`) |
| Model | Gemini 2.5 Flash (`gemini-2.5-flash`) |
| API Provider | Google AI Studio (API key auth) |
| Runtime | Python 3.11+ |
| Package Manager | `uv` |
| Web Framework | FastAPI (via ADK) |

## Project Structure

```
school-ai-assistant/
├── app/                    # Core agent application
│   ├── agent.py            # Root agent definition & ADK App
│   ├── fast_api_app.py     # FastAPI server entry point
│   ├── __init__.py         # Package exports
│   ├── .env                # Local environment variables (not committed)
│   └── app_utils/          # Utility helpers
├── tests/                  # Test suites
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── eval/               # Agent evaluation cases
├── docs/                   # Project documentation
│   └── architecture.md     # This file
├── .agents/                # Agent configuration & metadata
│   └── config.yaml         # Agent runtime config
├── GEMINI.md               # Guidance for Gemini coding assistant
├── README.md               # Project overview and quickstart
├── pyproject.toml          # Python project configuration
└── agents-cli-manifest.yaml # agents-cli project manifest
```

## Agent Design

The root agent (`school_ai_assistant`) follows a **single-agent pattern** with tools:

- `get_weather` — Example tool (to be replaced with school-specific tools)
- `get_current_time` — Example tool (to be replaced with school-specific tools)

### ADK 2.0 Patterns

- Uses `google.adk.agents.Agent` for the agent definition
- Uses `google.adk.apps.App` as the application container
- Session storage is **in-memory** (local dev only)
- Authentication via **Google AI Studio API key** (`.env` file)

## Local Development Flow

```
uv sync --group dev       # Install dependencies
agents-cli playground     # Launch local UI at http://localhost:8000
agents-cli run "prompt"   # Run single-turn prompt
pytest tests/             # Run tests
```
