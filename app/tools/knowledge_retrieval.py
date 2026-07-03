"""app/tools/knowledge_retrieval.py

MCP-ready knowledge retrieval layer for the School AI Assistant.

This module provides the `retrieve_knowledge` tool that specialist agents use to
search for school-specific documents (policies, curriculum guides, etc.) stored in
the project's `knowledge/` directory.

## Design Principles

- **Audience-scoped**: each call targets either `knowledge/parents/` or
  `knowledge/teachers/` — never both — to prevent cross-domain leakage.
- **Zero hardcoded filenames**: the directory is scanned dynamically with
  `pathlib.Path.iterdir()`.  Drop any new document into the folder and it
  will be picked up automatically.
- **Graceful empty-folder handling**: if no readable documents exist yet the
  tool returns ``status="no_documents"`` instead of raising an exception,
  so agents continue to function using their built-in knowledge.
- **Phase-3 upgrade path**: the public signature of `retrieve_knowledge` is
  intentionally stable.  In Phase 3 the internal body will be replaced with a
  real vector-search / embedding-store lookup (e.g. Vertex AI RAG or ChromaDB)
  without any changes to agent `tools=` lists or instruction prompts.

## Current Phase (Phase 2 — Infrastructure Only)

Text documents (`.txt`, `.md`) are read and returned verbatim as context
snippets.  PDF extraction is **not** implemented in this phase; PDF files are
detected and counted but their content is not yet extracted.  When PDFs are
ready to be indexed this module will be updated in Phase 3.

## MCP Integration Note

This function is designed to be wrapped as an MCP tool in a future deployment.
The dictionary return shape is stable and documented below.
"""

import pathlib
from typing import Literal

from app.app_utils.logging_config import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Project-layout constants
# ---------------------------------------------------------------------------
# Resolve the knowledge/ directory relative to this file's location so the
# tool works regardless of the working directory from which the app is run.
#
# Directory layout (all relative to project root):
#   knowledge/
#   ├── parents/    ← parent-facing policy / FAQ documents
#   └── teachers/   ← teacher-facing curriculum / lesson documents
#   app/
#   └── tools/
#       └── knowledge_retrieval.py  ← this file
#
# __file__ → .../app/tools/knowledge_retrieval.py
# parent   → .../app/tools/
# parent   → .../app/
# parent   → .../   (project root)
# / "knowledge" → .../knowledge/
_PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
_KNOWLEDGE_ROOT = _PROJECT_ROOT / "knowledge"

# Audience values the tool accepts — matches agent role names
AudienceType = Literal["parent", "teacher"]

# Text-based extensions we read directly in Phase 2.
# Binary formats (PDF) will be handled here.
_READABLE_EXTENSIONS: frozenset[str] = frozenset({".txt", ".md"})
_PDF_EXTENSION = ".pdf"

# Hard limit on characters returned per document to avoid bloating the
# context window.  Phase 3 will replace this with proper chunking.
_MAX_CHARS_PER_DOC = 4_000


def retrieve_knowledge(query: str, audience: str = "parent") -> dict:
    """Search the school knowledge base for documents relevant to *query*.

    This tool is called by specialist agents when they need school-specific
    factual context (policies, schedules, curriculum guides, etc.) that is
    not already covered by their built-in system prompt.

    Args:
        query:    The user's question or a short search phrase derived from it.
                  Used for future semantic search (Phase 3).  In Phase 2 it is
                  logged but not used for filtering.
        audience: Which knowledge folder to search — ``"parent"`` or
                  ``"teacher"``.  Defaults to ``"parent"``.

    Returns:
        dict with the following keys:

        - ``status`` (str): One of:
            - ``"ok"``           — at least one document was read successfully
            - ``"no_documents"`` — the folder exists but is empty (no PDFs yet)
            - ``"no_text_yet"``  — files exist but none are readable text (all PDF)
            - ``"folder_missing"`` — the audience folder does not exist at all
            - ``"error"``        — an unexpected I/O error occurred
        - ``audience`` (str):   The audience value that was used.
        - ``query`` (str):      Echo of the query (useful for logging / tracing).
        - ``source_count`` (int): Number of documents whose content is included.
        - ``results`` (list[dict]): One entry per readable document::

              {
                  "filename": str,   # basename only — no path information
                  "snippet":  str,   # first _MAX_CHARS_PER_DOC characters
              }

        - ``skipped_count`` (int): Files detected but not yet readable (e.g. PDF).
        - ``message`` (str):    Human-readable status description for the agent.
    """
    # ------------------------------------------------------------------
    # Normalise and validate the audience value
    # ------------------------------------------------------------------
    clean_audience = audience.strip().lower()
    if clean_audience not in ("parent", "teacher"):
        logger.warning(
            "event=retrieve_knowledge_invalid_audience | audience=%s", audience
        )
        return {
            "status": "error",
            "audience": audience,
            "query": query,
            "source_count": 0,
            "results": [],
            "skipped_count": 0,
            "message": (
                f"Unknown audience '{audience}'. "
                "Valid values are 'parent' or 'teacher'."
            ),
        }

    # Map audience → knowledge sub-folder
    folder_name = "parents" if clean_audience == "parent" else "teachers"
    knowledge_dir = _KNOWLEDGE_ROOT / folder_name

    logger.info(
        "event=retrieve_knowledge_started | audience=%s | query_len=%d | path=%s",
        clean_audience,
        len(query),
        knowledge_dir,
    )

    # ------------------------------------------------------------------
    # Guard: folder does not exist
    # ------------------------------------------------------------------
    if not knowledge_dir.exists():
        logger.warning(
            "event=retrieve_knowledge_folder_missing | path=%s", knowledge_dir
        )
        return {
            "status": "folder_missing",
            "audience": clean_audience,
            "query": query,
            "source_count": 0,
            "results": [],
            "skipped_count": 0,
            "message": (
                f"Knowledge folder '{folder_name}' does not exist. "
                "Please create it and add documents."
            ),
        }

    # ------------------------------------------------------------------
    # Scan directory for candidate files (non-recursive, Phase 2)
    # ------------------------------------------------------------------
    try:
        all_files = [
            f for f in knowledge_dir.iterdir()
            if f.is_file() and not f.name.startswith(".")
        ]
    except OSError as exc:
        logger.error(
            "event=retrieve_knowledge_io_error | path=%s | error=%s",
            knowledge_dir,
            exc,
        )
        return {
            "status": "error",
            "audience": clean_audience,
            "query": query,
            "source_count": 0,
            "results": [],
            "skipped_count": 0,
            "message": f"Could not read knowledge folder: {exc}",
        }

    if not all_files:
        logger.info(
            "event=retrieve_knowledge_no_documents | audience=%s", clean_audience
        )
        return {
            "status": "no_documents",
            "audience": clean_audience,
            "query": query,
            "source_count": 0,
            "results": [],
            "skipped_count": 0,
            "message": (
                "No documents are available yet. "
                "Please add school documents to the knowledge folder."
            ),
        }

    # ------------------------------------------------------------------
    # Read text documents; skip binary files (PDF will be Phase 3)
    # ------------------------------------------------------------------
    results: list[dict] = []
    skipped: list[str] = []

    for doc_path in sorted(all_files):
        suffix = doc_path.suffix.lower()
        # Handle PDF files separately
        if suffix == _PDF_EXTENSION:
            # Try to extract text from PDF using PyPDF2
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(str(doc_path))
                text_parts = []
                for page in reader.pages:
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as page_exc:
                        logger.debug(
                            "event=retrieve_knowledge_pdf_page_error | file=%s | error=%s",
                            doc_path.name,
                            page_exc,
                        )
                full_text = "\n".join(text_parts)
                snippet = full_text[:_MAX_CHARS_PER_DOC]
                results.append({"filename": doc_path.name, "snippet": snippet})
                logger.debug(
                    "event=retrieve_knowledge_pdf_read | file=%s | chars=%d",
                    doc_path.name,
                    len(snippet),
                )
            except Exception as exc:
                skipped.append(doc_path.name)
                logger.warning(
                    "event=retrieve_knowledge_pdf_error | file=%s | error=%s",
                    doc_path.name,
                    exc,
                )
            continue
        if suffix not in _READABLE_EXTENSIONS:
            # Binary or unsupported format — log and skip
            skipped.append(doc_path.name)
            logger.debug(
                "event=retrieve_knowledge_skipped | file=%s | reason=unsupported_format",
                doc_path.name,
            )
            continue

        try:
            text = doc_path.read_text(encoding="utf-8", errors="replace")
            snippet = text[:_MAX_CHARS_PER_DOC]
            results.append({"filename": doc_path.name, "snippet": snippet})
            logger.debug(
                "event=retrieve_knowledge_read | file=%s | chars=%d",
                doc_path.name,
                len(snippet),
            )
        except OSError as exc:
            skipped.append(doc_path.name)
            logger.warning(
                "event=retrieve_knowledge_read_error | file=%s | error=%s",
                doc_path.name,
                exc,
            )

    skipped_count = len(skipped)

    if not results:
        # Files exist but none were readable (all PDF or unreadable)
        logger.info(
            "event=retrieve_knowledge_no_text | audience=%s | skipped=%d",
            clean_audience,
            skipped_count,
        )
        return {
            "status": "no_text_yet",
            "audience": clean_audience,
            "query": query,
            "source_count": 0,
            "results": [],
            "skipped_count": skipped_count,
            "message": (
                f"{skipped_count} document(s) found but not yet readable. "
                "PDF indexing will be available in Phase 3."
            ),
        }

    logger.info(
        "event=retrieve_knowledge_completed | audience=%s | source_count=%d | skipped=%d",
        clean_audience,
        len(results),
        skipped_count,
    )
    return {
        "status": "ok",
        "audience": clean_audience,
        "query": query,
        "source_count": len(results),
        "results": results,
        "skipped_count": skipped_count,
        "message": f"Found {len(results)} document(s) for audience '{clean_audience}'.",
    }
