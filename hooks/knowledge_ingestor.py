#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Ingestor Hook (Stop)

Runs at session end. Parses the session transcript and extracts learnings:
  - Decisions made
  - Patterns used
  - Errors resolved
  - Files/features worked on

Creates knowledge fragments from extracted info and stores them in the
appropriate scope (shared for project decisions, personal for session context).
Deduplicates against existing fragments via fuzzy matching.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.knowledge_store import (
    DualKnowledgeStore,
    Fragment,
    find_similar,
    SCOPE_SHARED,
    SCOPE_PERSONAL
)
from utils.constants import ensure_session_log_dir


# Patterns for extracting learnings from transcripts
LEARNING_PATTERNS = [
    {
        "name": "decision",
        "patterns": [
            r"decided to (?:use|implement|go with|choose) (.+?)(?:\.|,|$)",
            r"(?:the|our) decision (?:is|was) to (.+?)(?:\.|,|$)",
            r"going (?:to|with) (.+?) (?:approach|pattern|method|solution)",
            r"(?:will|should) use (.+?) (?:for|to|when)",
        ],
        "tags": ["decision", "architecture"],
        "scope": SCOPE_SHARED
    },
    {
        "name": "pattern_used",
        "patterns": [
            r"using (?:the )?(.+?) pattern",
            r"implemented (?:using|with) (.+?)(?:\.|,|$)",
            r"following (?:the )?(.+?) (?:approach|convention|pattern)",
        ],
        "tags": ["pattern", "implementation"],
        "scope": SCOPE_SHARED
    },
    {
        "name": "error_resolved",
        "patterns": [
            r"(?:fixed|resolved|solved) (?:the )?(.+?) (?:error|issue|bug|problem)",
            r"(?:the )?(?:error|issue|bug) was (?:caused by|due to) (.+?)(?:\.|,|$)",
            r"(?:solution|fix) (?:is|was) to (.+?)(?:\.|,|$)",
        ],
        "tags": ["error", "debugging", "solution"],
        "scope": SCOPE_SHARED
    },
    {
        "name": "lesson_learned",
        "patterns": [
            r"learned that (.+?)(?:\.|,|$)",
            r"(?:remember|note) that (.+?)(?:\.|,|$)",
            r"(?:important|key) (?:thing|point|insight): (.+?)(?:\.|,|$)",
            r"(?:turns out|it seems) (?:that )?(.+?)(?:\.|,|$)",
        ],
        "tags": ["lesson", "insight"],
        "scope": SCOPE_SHARED
    },
    {
        "name": "workflow_preference",
        "patterns": [
            r"(?:i |I )prefer (?:to )?(.+?)(?:\.|,|$)",
            r"(?:my|the user's) preference is (.+?)(?:\.|,|$)",
            r"always (?:want|like) to (.+?)(?:\.|,|$)",
        ],
        "tags": ["workflow", "preference", "personal"],
        "scope": SCOPE_PERSONAL
    }
]

# File patterns mentioned in sessions
FILE_PATTERN = re.compile(r'(?:src/|\.claude/|\./)[\w/.-]+\.\w+')

# Minimum content length for a fragment
MIN_CONTENT_LENGTH = 20
MAX_CONTENT_LENGTH = 500


def extract_learnings_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extract potential learnings from text using pattern matching.

    Returns list of dicts with 'content', 'tags', 'scope'.
    """
    learnings = []

    for category in LEARNING_PATTERNS:
        for pattern in category["patterns"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                content = match.group(0).strip()

                # Filter by length
                if len(content) < MIN_CONTENT_LENGTH:
                    continue
                if len(content) > MAX_CONTENT_LENGTH:
                    content = content[:MAX_CONTENT_LENGTH] + "..."

                learnings.append({
                    "content": content,
                    "tags": category["tags"],
                    "scope": category["scope"],
                    "category": category["name"]
                })

    return learnings


def extract_files_from_text(text: str) -> List[str]:
    """Extract file paths mentioned in text."""
    matches = FILE_PATTERN.findall(text)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for path in matches:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique[:20]  # Limit to 20


def parse_transcript(transcript_path: str) -> str:
    """
    Parse JSONL transcript into text.

    Returns concatenated assistant messages.
    """
    text_parts = []

    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    msg = json.loads(line)
                    role = msg.get("role", "")

                    # Only extract from assistant messages
                    if role != "assistant":
                        continue

                    content = msg.get("content", msg.get("message", ""))

                    # Handle list content (tool use results)
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text_parts.append(item.get("text", ""))
                            elif isinstance(item, str):
                                text_parts.append(item)
                    elif isinstance(content, str):
                        text_parts.append(content)

                except json.JSONDecodeError:
                    continue

    except (OSError, IOError):
        pass

    return "\n".join(text_parts)


def create_session_fragments(
    learnings: List[Dict[str, Any]],
    files: List[str],
    session_id: str,
    store: DualKnowledgeStore
) -> List[Fragment]:
    """
    Create fragments from extracted learnings and store them.

    Deduplicates against existing fragments.
    Returns list of created fragments.
    """
    created = []

    for learning in learnings:
        content = learning["content"]
        tags = learning["tags"] + ["session-learned"]
        scope = learning["scope"]

        # Check for duplicates
        target_store = store.shared if scope == SCOPE_SHARED else store.personal
        if find_similar(content, target_store, threshold=0.6):
            continue

        # Create and store fragment
        fragment = Fragment(
            content=content,
            tags=tags,
            source=f"session:{session_id}",
            scope=scope
        )

        store.add(fragment)
        created.append(fragment)

    # Create a session summary fragment if files were worked on
    if files and len(created) > 0:
        summary = f"Session worked on {len(files)} files"
        if files[:5]:
            summary += ": " + ", ".join(os.path.basename(f) for f in files[:5])
            if len(files) > 5:
                summary += f" (+{len(files) - 5} more)"

        # Store as personal context
        if not find_similar(summary, store.personal, threshold=0.7):
            fragment = Fragment(
                content=summary,
                tags=["session-context", "files"],
                source=f"session:{session_id}",
                scope=SCOPE_PERSONAL
            )
            store.add(fragment)
            created.append(fragment)

    return created


def main():
    """Hook entry point - runs on Stop event."""
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        if not transcript_path or not os.path.exists(transcript_path):
            sys.exit(0)

        # Parse transcript
        text = parse_transcript(transcript_path)
        if not text or len(text) < 100:
            sys.exit(0)

        # Extract learnings
        learnings = extract_learnings_from_text(text)
        files = extract_files_from_text(text)

        if not learnings:
            sys.exit(0)

        # Create and store fragments
        store = DualKnowledgeStore()
        created = create_session_fragments(learnings, files, session_id, store)

        # Log results
        if created:
            try:
                log_dir = ensure_session_log_dir(session_id)
                log_file = log_dir / "knowledge_ingested.json"
                with open(log_file, "w") as f:
                    json.dump(
                        {
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "session_id": session_id,
                            "fragments_created": len(created),
                            "fragments": [
                                {"id": fr.id, "tags": fr.tags, "scope": fr.scope}
                                for fr in created
                            ],
                        },
                        f,
                        indent=2,
                    )
            except Exception:
                pass  # Don't fail if logging fails

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Knowledge ingestor error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
