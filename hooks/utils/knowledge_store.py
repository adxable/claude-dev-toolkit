#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Store - Fragment storage engine with TF-IDF indexing.

This module provides the core data model and storage engine for the semantic
memory system. It supports dual-store (shared + personal) with merge logic.

Zero external dependencies - uses only Python standard library.
"""

import json
import math
import re
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def get_toolkit_root() -> Path:
    """Get the toolkit root directory."""
    # hooks/utils/knowledge_store.py -> hooks/utils -> hooks -> toolkit root
    return Path(__file__).resolve().parent.parent.parent


def get_memory_dir() -> Path:
    """Get the memory directory."""
    return get_toolkit_root() / "memory"


def get_shared_knowledge_dir() -> Path:
    """Get the shared knowledge directory (committed to git)."""
    d = get_memory_dir() / "knowledge"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fragments").mkdir(parents=True, exist_ok=True)
    return d


def get_personal_knowledge_dir() -> Path:
    """Get the personal knowledge directory (gitignored)."""
    d = get_memory_dir() / "local"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fragments").mkdir(parents=True, exist_ok=True)
    return d


# Fragment scope types
SCOPE_SHARED = "shared"
SCOPE_PERSONAL = "personal"


class Fragment:
    """
    A knowledge fragment - the atomic unit of semantic memory.

    Attributes:
        id: Unique identifier
        content: The actual knowledge content
        tags: List of tags for categorization and boosting
        source: Where this knowledge came from (session, manual, file)
        scope: 'shared' (committed) or 'personal' (gitignored)
        created: ISO timestamp when created
        accessed_count: Number of times retrieved
        last_accessed: ISO timestamp of last retrieval
        metadata: Additional arbitrary metadata
    """

    def __init__(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        source: str = "manual",
        scope: str = SCOPE_SHARED,
        fragment_id: Optional[str] = None,
        created: Optional[str] = None,
        accessed_count: int = 0,
        last_accessed: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = fragment_id or str(uuid.uuid4())[:8]
        self.content = content
        self.tags = tags or []
        self.source = source
        self.scope = scope
        self.created = created or datetime.now().isoformat()
        self.accessed_count = accessed_count
        self.last_accessed = last_accessed
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize fragment to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "source": self.source,
            "scope": self.scope,
            "created": self.created,
            "accessed_count": self.accessed_count,
            "last_accessed": self.last_accessed,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fragment":
        """Deserialize fragment from dictionary."""
        return cls(
            content=data["content"],
            tags=data.get("tags", []),
            source=data.get("source", "unknown"),
            scope=data.get("scope", SCOPE_SHARED),
            fragment_id=data.get("id"),
            created=data.get("created"),
            accessed_count=data.get("accessed_count", 0),
            last_accessed=data.get("last_accessed"),
            metadata=data.get("metadata", {})
        )

    def mark_accessed(self) -> None:
        """Update access tracking."""
        self.accessed_count += 1
        self.last_accessed = datetime.now().isoformat()


class TFIDFIndex:
    """
    Simple TF-IDF index for semantic retrieval.

    Uses term frequency-inverse document frequency scoring to find
    relevant fragments based on query text.
    """

    def __init__(self):
        # term -> {fragment_id -> term_frequency}
        self.term_frequencies: Dict[str, Dict[str, float]] = defaultdict(dict)
        # fragment_id -> total terms
        self.doc_lengths: Dict[str, int] = {}
        # Total number of documents
        self.num_docs: int = 0
        # term -> number of documents containing term
        self.doc_frequencies: Dict[str, int] = defaultdict(int)

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Tokenize text into terms for indexing.

        Simple tokenization: lowercase, split on non-alphanumeric,
        filter short tokens and stopwords.
        """
        # Lowercase and split on non-alphanumeric
        tokens = re.findall(r'[a-z0-9]+', text.lower())

        # Simple stopwords list
        stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'this', 'that', 'these', 'those', 'it'
        }

        # Filter: min length 2, not stopword
        return [t for t in tokens if len(t) >= 2 and t not in stopwords]

    def add_document(self, doc_id: str, text: str, tags: Optional[List[str]] = None) -> None:
        """Add a document to the index."""
        # Combine content with tags for indexing
        full_text = text
        if tags:
            full_text += " " + " ".join(tags)

        tokens = self.tokenize(full_text)
        if not tokens:
            return

        # Count term frequencies
        term_counts: Dict[str, int] = defaultdict(int)
        for token in tokens:
            term_counts[token] += 1

        # Store normalized term frequencies
        doc_length = len(tokens)
        self.doc_lengths[doc_id] = doc_length

        # Track which terms we've seen in this doc (for doc frequency)
        seen_terms: set = set()

        for term, count in term_counts.items():
            # TF = count / doc_length (normalized)
            self.term_frequencies[term][doc_id] = count / doc_length

            if term not in seen_terms:
                self.doc_frequencies[term] += 1
                seen_terms.add(term)

        self.num_docs += 1

    def remove_document(self, doc_id: str) -> None:
        """Remove a document from the index."""
        if doc_id not in self.doc_lengths:
            return

        # Find all terms containing this doc
        terms_to_clean = []
        for term, docs in self.term_frequencies.items():
            if doc_id in docs:
                del docs[doc_id]
                self.doc_frequencies[term] -= 1
                if self.doc_frequencies[term] <= 0:
                    terms_to_clean.append(term)

        # Clean up empty terms
        for term in terms_to_clean:
            del self.term_frequencies[term]
            del self.doc_frequencies[term]

        del self.doc_lengths[doc_id]
        self.num_docs -= 1

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for documents matching the query.

        Returns list of (doc_id, score) tuples, sorted by score descending.
        """
        if self.num_docs == 0:
            return []

        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        # Calculate TF-IDF scores for each document
        scores: Dict[str, float] = defaultdict(float)

        for token in query_tokens:
            if token not in self.term_frequencies:
                continue

            # Smoothed IDF = log((N + 1) / (df + 1)) + 1
            # This ensures positive scores even with few documents
            df = self.doc_frequencies[token]
            idf = math.log((self.num_docs + 1) / (df + 1)) + 1

            for doc_id, tf in self.term_frequencies[token].items():
                # TF-IDF score
                scores[doc_id] += tf * idf

        # Sort by score descending
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_results[:top_k]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize index to dictionary."""
        return {
            "term_frequencies": {
                term: dict(docs) for term, docs in self.term_frequencies.items()
            },
            "doc_lengths": self.doc_lengths,
            "num_docs": self.num_docs,
            "doc_frequencies": dict(self.doc_frequencies)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TFIDFIndex":
        """Deserialize index from dictionary."""
        index = cls()
        index.term_frequencies = defaultdict(dict)
        for term, docs in data.get("term_frequencies", {}).items():
            index.term_frequencies[term] = docs
        index.doc_lengths = data.get("doc_lengths", {})
        index.num_docs = data.get("num_docs", 0)
        index.doc_frequencies = defaultdict(int)
        for term, count in data.get("doc_frequencies", {}).items():
            index.doc_frequencies[term] = count
        return index


class KnowledgeStore:
    """
    Knowledge store with TF-IDF indexing.

    Manages fragments with automatic index maintenance.
    """

    def __init__(self, scope: str = SCOPE_SHARED):
        """
        Initialize knowledge store for a specific scope.

        Args:
            scope: 'shared' or 'personal'
        """
        self.scope = scope
        self.base_dir = (
            get_shared_knowledge_dir() if scope == SCOPE_SHARED
            else get_personal_knowledge_dir()
        )
        self.fragments_dir = self.base_dir / "fragments"
        self.index_path = self.base_dir / "index.json"

        # Ensure directories exist
        self.fragments_dir.mkdir(parents=True, exist_ok=True)

        # Load or create index
        self.index = self._load_index()

    def _load_index(self) -> TFIDFIndex:
        """Load index from disk or create new."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    data = json.load(f)
                return TFIDFIndex.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        return TFIDFIndex()

    def _save_index(self) -> None:
        """Save index to disk."""
        with open(self.index_path, 'w') as f:
            json.dump(self.index.to_dict(), f, indent=2)

    def _fragment_path(self, fragment_id: str) -> Path:
        """Get path for a fragment file."""
        return self.fragments_dir / f"{fragment_id}.json"

    def add(self, fragment: Fragment) -> str:
        """
        Add a fragment to the store.

        Returns the fragment ID.
        """
        # Ensure scope matches store
        fragment.scope = self.scope

        # Save fragment
        path = self._fragment_path(fragment.id)
        with open(path, 'w') as f:
            json.dump(fragment.to_dict(), f, indent=2)

        # Update index
        self.index.add_document(fragment.id, fragment.content, fragment.tags)
        self._save_index()

        return fragment.id

    def get(self, fragment_id: str) -> Optional[Fragment]:
        """Get a fragment by ID."""
        path = self._fragment_path(fragment_id)
        if not path.exists():
            return None

        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return Fragment.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def update(self, fragment: Fragment) -> bool:
        """
        Update an existing fragment.

        Returns True if successful, False if fragment doesn't exist.
        """
        path = self._fragment_path(fragment.id)
        if not path.exists():
            return False

        # Update index (remove old, add new)
        self.index.remove_document(fragment.id)
        self.index.add_document(fragment.id, fragment.content, fragment.tags)

        # Save fragment
        with open(path, 'w') as f:
            json.dump(fragment.to_dict(), f, indent=2)

        self._save_index()
        return True

    def delete(self, fragment_id: str) -> bool:
        """
        Delete a fragment.

        Returns True if successful, False if fragment doesn't exist.
        """
        path = self._fragment_path(fragment_id)
        if not path.exists():
            return False

        # Remove from index
        self.index.remove_document(fragment_id)
        self._save_index()

        # Delete file
        path.unlink()
        return True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Fragment, float]]:
        """
        Search for fragments matching the query.

        Returns list of (fragment, score) tuples.
        """
        results = self.index.search(query, top_k)

        fragments = []
        for doc_id, score in results:
            fragment = self.get(doc_id)
            if fragment:
                fragments.append((fragment, score))

        return fragments

    def list_all(self) -> List[Fragment]:
        """List all fragments in the store."""
        fragments = []
        if self.fragments_dir.exists():
            for path in self.fragments_dir.glob("*.json"):
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                    fragments.append(Fragment.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    continue
        return fragments

    def rebuild_index(self) -> int:
        """
        Rebuild the index from all fragments.

        Returns the number of fragments indexed.
        """
        self.index = TFIDFIndex()

        count = 0
        for fragment in self.list_all():
            self.index.add_document(fragment.id, fragment.content, fragment.tags)
            count += 1

        self._save_index()
        return count

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the store."""
        fragments = self.list_all()

        # Collect tag counts
        tag_counts: Dict[str, int] = defaultdict(int)
        source_counts: Dict[str, int] = defaultdict(int)
        total_accessed = 0

        for f in fragments:
            for tag in f.tags:
                tag_counts[tag] += 1
            source_counts[f.source] += 1
            total_accessed += f.accessed_count

        return {
            "scope": self.scope,
            "total_fragments": len(fragments),
            "total_terms": len(self.index.term_frequencies),
            "tag_counts": dict(tag_counts),
            "source_counts": dict(source_counts),
            "total_accesses": total_accessed
        }


class DualKnowledgeStore:
    """
    Unified interface for querying both shared and personal knowledge stores.

    Implements merge logic where shared fragments generally rank higher for
    project knowledge, but personal fragments can rank higher for workflow
    preferences.
    """

    def __init__(self):
        self.shared = KnowledgeStore(SCOPE_SHARED)
        self.personal = KnowledgeStore(SCOPE_PERSONAL)

    def add(self, fragment: Fragment) -> str:
        """Add a fragment to the appropriate store based on its scope."""
        if fragment.scope == SCOPE_PERSONAL:
            return self.personal.add(fragment)
        return self.shared.add(fragment)

    def get(self, fragment_id: str) -> Optional[Fragment]:
        """Get a fragment by ID from either store."""
        # Try shared first
        fragment = self.shared.get(fragment_id)
        if fragment:
            return fragment
        return self.personal.get(fragment_id)

    def search(
        self,
        query: str,
        top_k: int = 5,
        shared_boost: float = 1.2,
        personal_tags_boost: Optional[List[str]] = None
    ) -> List[Tuple[Fragment, float]]:
        """
        Search both stores and merge results.

        Args:
            query: Search query
            top_k: Maximum results to return
            shared_boost: Score multiplier for shared fragments
            personal_tags_boost: Tags that boost personal fragment scores

        Returns list of (fragment, score) tuples, merged and sorted.
        """
        personal_tags_boost = personal_tags_boost or ['workflow', 'preference', 'personal']

        # Get results from both stores
        shared_results = self.shared.search(query, top_k * 2)
        personal_results = self.personal.search(query, top_k * 2)

        # Apply boosts
        merged: List[Tuple[Fragment, float]] = []

        for fragment, score in shared_results:
            # Shared fragments get boost for project knowledge
            merged.append((fragment, score * shared_boost))

        for fragment, score in personal_results:
            # Personal fragments get boost if they have preference tags
            boost = 1.0
            if any(tag in fragment.tags for tag in personal_tags_boost):
                boost = 1.3  # Personal preference boost
            merged.append((fragment, score * boost))

        # Sort by score descending and deduplicate by ID
        seen_ids: set = set()
        final_results: List[Tuple[Fragment, float]] = []

        for fragment, score in sorted(merged, key=lambda x: x[1], reverse=True):
            if fragment.id not in seen_ids:
                seen_ids.add(fragment.id)
                final_results.append((fragment, score))
            if len(final_results) >= top_k:
                break

        return final_results

    def promote(self, fragment_id: str) -> bool:
        """
        Promote a personal fragment to shared.

        Returns True if successful.
        """
        fragment = self.personal.get(fragment_id)
        if not fragment:
            return False

        # Delete from personal
        self.personal.delete(fragment_id)

        # Add to shared
        fragment.scope = SCOPE_SHARED
        self.shared.add(fragment)

        return True

    def get_all_stats(self) -> Dict[str, Any]:
        """Get combined statistics from both stores."""
        shared_stats = self.shared.get_stats()
        personal_stats = self.personal.get_stats()

        return {
            "shared": shared_stats,
            "personal": personal_stats,
            "combined": {
                "total_fragments": (
                    shared_stats["total_fragments"] +
                    personal_stats["total_fragments"]
                ),
                "total_terms": (
                    shared_stats["total_terms"] +
                    personal_stats["total_terms"]
                )
            }
        }


def find_similar(content: str, store: KnowledgeStore, threshold: float = 0.5) -> Optional[Fragment]:
    """
    Find a similar fragment in the store (for deduplication).

    Uses TF-IDF search and checks if top result exceeds threshold.
    """
    results = store.search(content, top_k=1)
    if results and results[0][1] >= threshold:
        return results[0][0]
    return None


def create_fragment(
    content: str,
    tags: Optional[List[str]] = None,
    source: str = "manual",
    scope: str = SCOPE_SHARED
) -> Fragment:
    """Create a new fragment."""
    return Fragment(content=content, tags=tags, source=source, scope=scope)
