#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
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

from utils.constants import ensure_session_log_dir
from utils.knowledge_store import add_fragment, is_duplicate

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Transcript parsing
# ---------------------------------------------------------------------------

def parse_transcript(transcript_path: str) -> List[Dict[str, Any]]:
    """Parse JSONL transcript into messages."""
    messages: List[Dict[str, Any]] = []
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except (OSError, IOError):
        pass
    return messages


# ---------------------------------------------------------------------------
# Extraction heuristics
# ---------------------------------------------------------------------------

def extract_decisions(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Find decision-like statements in assistant messages."""
    decisions: List[Dict[str, str]] = []
    decision_patterns = [
        r"(?:decided|choosing|going with|using|picked|selected|opting for)\s+(.{10,120})",
        r"(?:the approach|the solution|the fix|the pattern)\s+(?:is|will be)\s+(.{10,120})",
        r"(?:instead of|rather than)\s+(.{10,80}),?\s+(?:we|I)(?:'ll)?\s+(.{10,80})",
    ]

    for msg in messages:
        content = _extract_text(msg)
        if not content or msg.get("role") == "user":
            continue
        for pattern in decision_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                text = match.group(0).strip()
                if len(text) > 20:
                    decisions.append({
                        "content": text[:300],
                        "type": "decision",
                    })

    return decisions[:5]


def extract_error_resolutions(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Find error -> fix pairs in the session."""
    resolutions: List[Dict[str, str]] = []
    error_context: Optional[str] = None

    for msg in messages:
        content = _extract_text(msg)
        if not content:
            continue

        if re.search(r"(?:error|failed|exception|traceback|cannot|unable)", content, re.IGNORECASE):
            for line in content.split("\n"):
                if re.search(r"(?:error|Error|failed|Failed|Exception)", line):
                    error_context = line.strip()[:200]
                    break

        if error_context and msg.get("role") != "user":
            fix_patterns = [
                r"(?:fix|fixed|resolved|solution|the issue was|the problem was)\s+(.{10,150})",
            ]
            for pattern in fix_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    resolutions.append({
                        "content": f"Error: {error_context}\nResolution: {match.group(0).strip()[:200]}",
                        "type": "error_resolution",
                    })
                    error_context = None
                    break

    return resolutions[:5]


def extract_files_worked_on(messages: List[Dict[str, Any]]) -> List[str]:
    """Extract file paths from tool use messages."""
    files: List[str] = []
    for msg in messages:
        if msg.get("type") == "tool_use" or "tool" in msg:
            tool_input = msg.get("input", {})
            if isinstance(tool_input, dict):
                path = tool_input.get("file_path", tool_input.get("path", ""))
                if path and path not in files:
                    files.append(path)
    return files[:20]


def extract_patterns_used(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Detect coding patterns mentioned in assistant messages."""
    patterns_found: List[Dict[str, str]] = []
    pattern_keywords = [
        r"(?:pattern|approach|technique|strategy|method):\s*(.{10,150})",
        r"(?:following the|using the|applying the)\s+(\w[\w\s\-]+(?:pattern|approach|technique|convention))",
    ]

    for msg in messages:
        content = _extract_text(msg)
        if not content or msg.get("role") == "user":
            continue
        for pk in pattern_keywords:
            for match in re.finditer(pk, content, re.IGNORECASE):
                text = match.group(0).strip()[:200]
                if len(text) > 15:
                    patterns_found.append({
                        "content": text,
                        "type": "pattern",
                    })

    return patterns_found[:5]


def _extract_text(msg: Dict[str, Any]) -> Optional[str]:
    """Pull text content from various message formats."""
    content = msg.get("content", msg.get("message", msg.get("output", "")))
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    if isinstance(content, str):
        return content
    return None


# ---------------------------------------------------------------------------
# Fragment creation
# ---------------------------------------------------------------------------

def create_session_fragments(
    decisions: List[Dict[str, str]],
    resolutions: List[Dict[str, str]],
    patterns: List[Dict[str, str]],
    files: List[str],
    session_id: str,
) -> List[Dict[str, Any]]:
    """Turn extracted info into knowledge fragments and store them."""
    created: List[Dict[str, Any]] = []

    for d in decisions:
        if is_duplicate(d["content"], "shared"):
            continue
        frag = add_fragment(
            content=d["content"],
            tags=["decision", "session-learned"],
            source=f"session:{session_id}",
            scope="shared",
        )
        created.append(frag)

    for r in resolutions:
        if is_duplicate(r["content"], "shared"):
            continue
        frag = add_fragment(
            content=r["content"],
            tags=["error-resolution", "debugging", "session-learned"],
            source=f"session:{session_id}",
            scope="shared",
        )
        created.append(frag)

    for p in patterns:
        if is_duplicate(p["content"], "shared"):
            continue
        frag = add_fragment(
            content=p["content"],
            tags=["pattern", "session-learned"],
            source=f"session:{session_id}",
            scope="shared",
        )
        created.append(frag)

    if files:
        summary = f"Session {session_id}: worked on {len(files)} files"
        if files[:5]:
            summary += " including " + ", ".join(os.path.basename(f) for f in files[:5])
        if not is_duplicate(summary, "personal"):
            frag = add_fragment(
                content=summary,
                tags=["session-context", "files"],
                source=f"session:{session_id}",
                scope="personal",
            )
            created.append(frag)

    return created


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        if not transcript_path or not os.path.exists(transcript_path):
            sys.exit(0)

        messages = parse_transcript(transcript_path)
        if not messages:
            sys.exit(0)

        decisions = extract_decisions(messages)
        resolutions = extract_error_resolutions(messages)
        patterns = extract_patterns_used(messages)
        files = extract_files_worked_on(messages)

        created = create_session_fragments(
            decisions, resolutions, patterns, files, session_id
        )

        if created:
            log_dir = ensure_session_log_dir(session_id)
            log_file = log_dir / "knowledge_ingested.json"
            with open(log_file, "w") as f:
                json.dump(
                    {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "session_id": session_id,
                        "fragments_created": len(created),
                        "fragments": [
                            {"id": fr["id"], "tags": fr["tags"], "scope": fr["scope"]}
                            for fr in created
                        ],
                    },
                    f,
                    indent=2,
                )

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Error in knowledge_ingestor: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
