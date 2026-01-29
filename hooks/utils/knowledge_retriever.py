#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Retriever

Query engine that finds relevant knowledge fragments for a given prompt.
Uses TF-IDF scoring with tag boosting and recency weighting.
Queries both shared and personal stores, merging results with priority.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from utils.constants import get_knowledge_dir, get_local_dir
from utils.knowledge_store import (
    load_fragment,
    load_index,
    term_frequencies,
    tokenize,
    touch_fragment,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MAX_RESULTS = 5
TAG_BOOST = 0.3          # Added to score when a query token matches a tag
RECENCY_BOOST = 0.1      # Max boost for recently-accessed fragments
SHARED_PRIORITY = 1.05   # Multiplier for shared (project-level) fragments


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _tfidf_score(
    query_tf: Dict[str, float],
    doc_tf: Dict[str, float],
    idf: Dict[str, float],
) -> float:
    """Compute TF-IDF cosine-like score between query and document."""
    score = 0.0
    for term, q_freq in query_tf.items():
        if term in doc_tf:
            term_idf = idf.get(term, 1.0)
            score += q_freq * doc_tf[term] * term_idf
    return score


def _tag_score(query_tokens: List[str], tags: List[str]) -> float:
    """Bonus score when query tokens overlap with fragment tags."""
    if not tags:
        return 0.0
    tag_tokens = set()
    for tag in tags:
        tag_tokens.update(t.lower() for t in tag.split("-"))
        tag_tokens.update(t.lower() for t in tag.split("_"))
        tag_tokens.add(tag.lower())
    overlap = sum(1 for t in query_tokens if t in tag_tokens)
    return min(overlap * TAG_BOOST, TAG_BOOST * 3)  # cap at 3 tag matches


def _recency_score(fragment: Optional[Dict[str, Any]]) -> float:
    """Small boost for recently-accessed fragments (decays over 7 days)."""
    if not fragment or not fragment.get("last_accessed"):
        return 0.0
    try:
        accessed = datetime.fromisoformat(
            fragment["last_accessed"].replace("Z", "+00:00")
        )
        now = datetime.utcnow().replace(tzinfo=accessed.tzinfo)
        age_days = (now - accessed).total_seconds() / 86400
        if age_days < 7:
            return RECENCY_BOOST * (1 - age_days / 7)
    except (ValueError, TypeError):
        pass
    return 0.0


# ---------------------------------------------------------------------------
# Main retrieval
# ---------------------------------------------------------------------------

def retrieve(
    prompt: str,
    max_results: int = MAX_RESULTS,
    tag_filter: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Find the most relevant knowledge fragments for *prompt*.

    Returns a list of dicts:
        { "id", "content", "tags", "scope", "score" }
    sorted by descending score.
    """
    query_tokens = tokenize(prompt)
    if not query_tokens:
        return []

    query_tf = term_frequencies(query_tokens)

    scored: List[Tuple[float, str, str, Dict[str, Any]]] = []

    for scope, base_dir in [("shared", get_knowledge_dir()), ("personal", get_local_dir())]:
        index = load_index(base_dir)
        idf = index.get("idf", {})

        for frag_id, fdata in index.get("fragments", {}).items():
            doc_tf = fdata.get("tf", {})
            tags = fdata.get("tags", [])

            if tag_filter:
                if not any(t in tags for t in tag_filter):
                    continue

            score = _tfidf_score(query_tf, doc_tf, idf)
            if score <= 0:
                continue

            score += _tag_score(query_tokens, tags)

            frag = load_fragment(base_dir, frag_id)
            score += _recency_score(frag)

            if scope == "shared":
                score *= SHARED_PRIORITY

            scored.append((score, frag_id, scope, fdata))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    seen_ids = set()
    for score, frag_id, scope, fdata in scored[:max_results]:
        if frag_id in seen_ids:
            continue
        seen_ids.add(frag_id)

        base_dir = get_knowledge_dir() if scope == "shared" else get_local_dir()
        frag = load_fragment(base_dir, frag_id)
        if not frag:
            continue

        touch_fragment(frag_id, scope)

        results.append({
            "id": frag_id,
            "content": frag["content"],
            "tags": frag.get("tags", []),
            "scope": scope,
            "score": round(score, 4),
        })

    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_results(results: List[Dict[str, Any]]) -> str:
    """Format retrieval results as concise context for injection into a prompt."""
    if not results:
        return ""

    lines = [
        "",
        "─" * 50,
        "RELEVANT KNOWLEDGE",
        "─" * 50,
        "",
    ]

    for i, r in enumerate(results, 1):
        scope_badge = "[shared]" if r["scope"] == "shared" else "[personal]"
        tags_str = ", ".join(r["tags"][:5]) if r["tags"] else "none"
        lines.append(f"  {i}. {scope_badge} (tags: {tags_str})")
        content = r["content"].strip()
        for para in content.split("\n"):
            lines.append(f"     {para}")
        lines.append("")

    lines.append("─" * 50)
    return "\n".join(lines)
