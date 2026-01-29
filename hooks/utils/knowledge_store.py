#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Fragment Store

Core data model and storage engine for the semantic memory system.
Manages CRUD operations on knowledge fragments and maintains a TF-IDF index
for fast retrieval. Zero external dependencies.

Dual-store design:
  - memory/knowledge/ (shared, committed to git)
  - memory/local/     (personal, gitignored)
"""

import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.constants import get_knowledge_dir, get_local_dir


# ---------------------------------------------------------------------------
# Data model helpers
# ---------------------------------------------------------------------------

def _new_id(content: str) -> str:
    """Generate a deterministic short id from content."""
    return hashlib.sha256(content.encode()).hexdigest()[:12]


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def create_fragment(
    content: str,
    tags: List[str],
    source: str = "manual",
    scope: str = "shared",
) -> Dict[str, Any]:
    """Create a new knowledge fragment dict."""
    return {
        "id": _new_id(content),
        "content": content,
        "tags": [t.lower().strip() for t in tags],
        "source": source,
        "scope": scope,
        "created": _now_iso(),
        "accessed_count": 0,
        "last_accessed": None,
    }


# ---------------------------------------------------------------------------
# Tokenisation & TF-IDF helpers
# ---------------------------------------------------------------------------

_STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did "
    "will would shall should may might can could of in to for on with "
    "at by from as into about between through during after before this "
    "that it its and or but not no nor so if then else when what which "
    "who whom how all each every both few more most other some such "
    "than too very just also only".split()
)


def tokenize(text: str) -> List[str]:
    """Lowercase, strip punctuation, remove stop-words."""
    tokens = re.findall(r"[a-z0-9][a-z0-9_\-]*", text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]


def term_frequencies(tokens: List[str]) -> Dict[str, float]:
    """Compute normalised term-frequency vector."""
    if not tokens:
        return {}
    counts: Dict[str, int] = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    total = len(tokens)
    return {t: c / total for t, c in counts.items()}


# ---------------------------------------------------------------------------
# Index management
# ---------------------------------------------------------------------------

def _index_path(base_dir: Path) -> Path:
    return base_dir / "index.json"


def load_index(base_dir: Path) -> Dict[str, Any]:
    """Load the TF-IDF index from disk.

    Index structure:
    {
        "fragments": { "<id>": { "tf": { "<term>": <freq> }, "tags": [...] } },
        "idf": { "<term>": <idf_value> },
        "doc_count": <int>,
        "updated": "<iso>"
    }
    """
    path = _index_path(base_dir)
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"fragments": {}, "idf": {}, "doc_count": 0, "updated": _now_iso()}


def save_index(base_dir: Path, index: Dict[str, Any]) -> None:
    index["updated"] = _now_iso()
    with open(_index_path(base_dir), "w") as f:
        json.dump(index, f, indent=2)


def rebuild_idf(index: Dict[str, Any]) -> None:
    """Recompute IDF values from the current fragment set."""
    doc_count = len(index["fragments"])
    if doc_count == 0:
        index["idf"] = {}
        index["doc_count"] = 0
        return

    df: Dict[str, int] = {}
    for fdata in index["fragments"].values():
        for term in fdata.get("tf", {}):
            df[term] = df.get(term, 0) + 1

    index["idf"] = {
        term: math.log((doc_count + 1) / (count + 1)) + 1
        for term, count in df.items()
    }
    index["doc_count"] = doc_count


# ---------------------------------------------------------------------------
# Fragment file I/O
# ---------------------------------------------------------------------------

def _fragment_path(base_dir: Path, frag_id: str) -> Path:
    return base_dir / "fragments" / f"{frag_id}.json"


def save_fragment(base_dir: Path, fragment: Dict[str, Any]) -> None:
    path = _fragment_path(base_dir, fragment["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(fragment, f, indent=2)


def load_fragment(base_dir: Path, frag_id: str) -> Optional[Dict[str, Any]]:
    path = _fragment_path(base_dir, frag_id)
    if not path.exists():
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def list_fragments(base_dir: Path) -> List[Dict[str, Any]]:
    """Load all fragments from a directory."""
    frags_dir = base_dir / "fragments"
    if not frags_dir.exists():
        return []
    results = []
    for p in frags_dir.glob("*.json"):
        try:
            with open(p, "r") as f:
                results.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue
    return results


def delete_fragment(base_dir: Path, frag_id: str) -> bool:
    path = _fragment_path(base_dir, frag_id)
    if path.exists():
        path.unlink()
        return True
    return False


# ---------------------------------------------------------------------------
# CRUD operations (high-level)
# ---------------------------------------------------------------------------

def _dir_for_scope(scope: str) -> Path:
    return get_knowledge_dir() if scope == "shared" else get_local_dir()


def add_fragment(
    content: str,
    tags: List[str],
    source: str = "manual",
    scope: str = "shared",
) -> Dict[str, Any]:
    """Create a fragment, persist it, and update the index."""
    base = _dir_for_scope(scope)
    fragment = create_fragment(content, tags, source, scope)

    # Check for duplicate id (same content hash)
    existing = load_fragment(base, fragment["id"])
    if existing:
        merged_tags = list(set(existing["tags"] + fragment["tags"]))
        existing["tags"] = merged_tags
        save_fragment(base, existing)
        _index_fragment(base, existing)
        return existing

    save_fragment(base, fragment)
    _index_fragment(base, fragment)
    return fragment


def get_fragment(frag_id: str, scope: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get a fragment by id. Searches both stores if scope is None."""
    if scope:
        return load_fragment(_dir_for_scope(scope), frag_id)
    frag = load_fragment(get_knowledge_dir(), frag_id)
    if frag:
        return frag
    return load_fragment(get_local_dir(), frag_id)


def remove_fragment(frag_id: str, scope: str = "shared") -> bool:
    """Delete a fragment and update the index."""
    base = _dir_for_scope(scope)
    deleted = delete_fragment(base, frag_id)
    if deleted:
        index = load_index(base)
        index["fragments"].pop(frag_id, None)
        rebuild_idf(index)
        save_index(base, index)
    return deleted


def touch_fragment(frag_id: str, scope: Optional[str] = None) -> None:
    """Record an access on a fragment (updates accessed_count and last_accessed)."""
    if scope:
        dirs = [_dir_for_scope(scope)]
    else:
        dirs = [get_knowledge_dir(), get_local_dir()]

    for base in dirs:
        frag = load_fragment(base, frag_id)
        if frag:
            frag["accessed_count"] = frag.get("accessed_count", 0) + 1
            frag["last_accessed"] = _now_iso()
            save_fragment(base, frag)
            return


def promote_fragment(frag_id: str) -> Optional[Dict[str, Any]]:
    """Move a personal fragment to shared scope."""
    local = get_local_dir()
    shared = get_knowledge_dir()

    frag = load_fragment(local, frag_id)
    if not frag:
        return None

    frag["scope"] = "shared"
    save_fragment(shared, frag)
    _index_fragment(shared, frag)

    delete_fragment(local, frag_id)
    local_index = load_index(local)
    local_index["fragments"].pop(frag_id, None)
    rebuild_idf(local_index)
    save_index(local, local_index)

    return frag


# ---------------------------------------------------------------------------
# Indexing helpers
# ---------------------------------------------------------------------------

def _index_fragment(base_dir: Path, fragment: Dict[str, Any]) -> None:
    """Add/update a single fragment in the index."""
    index = load_index(base_dir)
    tokens = tokenize(fragment["content"])
    for tag in fragment.get("tags", []):
        tokens.extend(tokenize(tag))

    tf = term_frequencies(tokens)
    index["fragments"][fragment["id"]] = {
        "tf": tf,
        "tags": fragment.get("tags", []),
    }
    rebuild_idf(index)
    save_index(base_dir, index)


def rebuild_full_index(scope: str = "shared") -> Dict[str, Any]:
    """Rebuild the entire index from fragment files on disk."""
    base = _dir_for_scope(scope)
    frags = list_fragments(base)

    index: Dict[str, Any] = {
        "fragments": {},
        "idf": {},
        "doc_count": 0,
        "updated": _now_iso(),
    }

    for frag in frags:
        tokens = tokenize(frag["content"])
        for tag in frag.get("tags", []):
            tokens.extend(tokenize(tag))
        tf = term_frequencies(tokens)
        index["fragments"][frag["id"]] = {
            "tf": tf,
            "tags": frag.get("tags", []),
        }

    rebuild_idf(index)
    save_index(base, index)
    return index


# ---------------------------------------------------------------------------
# Fuzzy deduplication
# ---------------------------------------------------------------------------

def is_duplicate(content: str, scope: str = "shared", threshold: float = 0.7) -> Optional[str]:
    """Check if content is a near-duplicate of an existing fragment.

    Returns the id of the duplicate fragment if found, else None.
    Uses Jaccard similarity on token sets.
    """
    base = _dir_for_scope(scope)
    new_tokens = set(tokenize(content))
    if not new_tokens:
        return None

    frags = list_fragments(base)
    for frag in frags:
        existing_tokens = set(tokenize(frag["content"]))
        if not existing_tokens:
            continue
        intersection = new_tokens & existing_tokens
        union = new_tokens | existing_tokens
        similarity = len(intersection) / len(union)
        if similarity >= threshold:
            return frag["id"]

    return None
