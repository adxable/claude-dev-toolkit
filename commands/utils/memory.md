# Memory

Manage project memory - decisions, lessons, and the semantic knowledge store.

## Arguments

- `decision "description"` - Add a new decision
- `lesson "description"` - Add a new lesson
- `add "content" --tags tag1,tag2` - Add a knowledge fragment
- `search "query"` - Search the knowledge store
- `show` - Show current memory + fragment stats
- `sync` - Rebuild index from fragment files
- `promote {id}` - Promote personal fragment to shared
- `skip` - Dismiss memory update prompt

## Instructions

### Add Decision

Append to `.claude/memory/decisions.md`:

```markdown
## {date} - {description}

Context: {current task/feature}
Reason: {why this decision was made}
```

**Example usage:**
```
/memory decision "Use TanStack Query queryOptions factory pattern"
```

**Writes:**
```markdown
## 2026-01-20 - Use TanStack Query queryOptions factory pattern

Context: Implementing data fetching layer
Reason: Provides better type inference and query key organization
```

### Add Lesson

Append to `.claude/memory/lessons.md`:

```markdown
## {date} - {description}

Context: {what happened}
Solution: {how it was resolved}
Prevention: {how to avoid in future}
```

**Example usage:**
```
/memory lesson "Zustand without useShallow causes infinite re-renders"
```

**Writes:**
```markdown
## 2026-01-20 - Zustand without useShallow causes infinite re-renders

Context: Object selector in Zustand store causing component re-render loop
Solution: Wrapped selector with useShallow from zustand/shallow
Prevention: Always use useShallow when selecting object/array from Zustand
```

### Add Knowledge Fragment

Add a fragment to the semantic knowledge store:

```
/memory add "Use JWT with short-lived tokens for API auth" --tags authentication,api,security
```

Stores the fragment in `memory/knowledge/fragments/` (shared) by default.
Use `--scope personal` to store in `memory/local/fragments/` instead.

**Implementation:**
```python
from utils.knowledge_store import add_fragment
add_fragment(content="...", tags=["tag1", "tag2"], source="manual", scope="shared")
```

### Search Knowledge Store

Perform semantic (TF-IDF) search across both shared and personal stores:

```
/memory search "How should I handle authentication?"
```

Returns top 5 matches ranked by relevance with tag boosting and recency weighting.

**Implementation:**
```python
from utils.knowledge_retriever import retrieve, format_results
results = retrieve("query text")
print(format_results(results))
```

### Show Memory

Display current contents of:
- `.claude/memory/decisions.md`
- `.claude/memory/lessons.md`
- `.claude/context/session_context.json` (patterns)
- Knowledge store stats (shared + personal fragment counts)

**Output format:**
```
┌─────────────────────────────────────────────────────────────┐
│  PROJECT MEMORY                                              │
├─────────────────────────────────────────────────────────────┤
│  DECISIONS (5 total)                                         │
│                                                              │
│  Recent:                                                     │
│  * 2026-01-20: Use TanStack Query queryOptions factory       │
│  * 2026-01-18: Feature-based folder structure                │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  LESSONS (3 total)                                           │
│                                                              │
│  Recent:                                                     │
│  * 2026-01-20: Zustand + useShallow for object selectors     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  KNOWLEDGE STORE                                             │
│                                                              │
│  * Shared fragments: 12                                      │
│  * Personal fragments: 5                                     │
│  * Index terms: 87                                           │
│  * Last updated: 2026-01-20T14:30:00Z                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  ESTABLISHED PATTERNS                                        │
│                                                              │
│  * dataFetching: TanStack Query with queryOptions            │
│  * stateManagement: Zustand with useShallow                  │
└─────────────────────────────────────────────────────────────┘
```

### Sync Index

Rebuild the TF-IDF index from all fragment files on disk. Use after manual edits to fragment JSON files.

```
/memory sync
```

**Implementation:**
```python
from utils.knowledge_store import rebuild_full_index
rebuild_full_index("shared")
rebuild_full_index("personal")
```

### Promote Fragment

Move a personal fragment to the shared store so the whole team benefits:

```
/memory promote abc123def456
```

The fragment moves from `memory/local/fragments/` to `memory/knowledge/fragments/` and will be committed to git.

**Implementation:**
```python
from utils.knowledge_store import promote_fragment
promote_fragment("fragment-id")
```

### Skip

Dismiss the memory update prompt without adding anything.

## Data Location

Memory is stored in:
```
memory/
├── CLAUDE.md              # L1 - always loaded (project context)
├── decisions.md           # L1 - always loaded (ADRs)
├── conventions.md         # L1 - always loaded (code patterns)
├── lessons.md             # L1 - always loaded (learnings)
├── knowledge/             # L2 - semantic knowledge store (shared)
│   ├── index.json         # TF-IDF index
│   └── fragments/         # Individual fragment JSON files
├── local/                 # L3 - personal knowledge (gitignored)
│   ├── index.json         # Personal index
│   └── fragments/         # Personal fragment files
└── README.md              # System documentation
```

## How the Knowledge Store Works

### Automatic Retrieval (every prompt)
The `knowledge_loader.py` hook runs on `UserPromptSubmit`:
1. Tokenizes the user's prompt
2. Scores indexed fragments using TF-IDF
3. Applies tag boosting and recency weighting
4. Shared fragments rank higher than personal
5. Returns top 5 fragments as context

### Automatic Ingestion (session end)
The `knowledge_ingestor.py` hook runs on `Stop`:
1. Parses the session transcript
2. Extracts decisions, error resolutions, patterns
3. Creates knowledge fragments with appropriate tags
4. Deduplicates against existing fragments (Jaccard similarity)

### Fragment Format
```json
{
  "id": "abc123def456",
  "content": "Use JWT with short-lived tokens for API auth",
  "tags": ["decision", "authentication"],
  "source": "session:abc123",
  "scope": "shared",
  "created": "2025-01-23T10:00:00Z",
  "accessed_count": 3,
  "last_accessed": "2025-01-25T14:30:00Z"
}
```

## Integration

Memory files are automatically read by:
- `context_loader.py` hook (injects into prompts)
- `knowledge_loader.py` hook (semantic fragment retrieval)
- `knowledge_ingestor.py` hook (extracts session learnings)
- `/plan` command (considers past decisions)
- Code reviewer agent (checks for pattern consistency)

## Output

```
┌─────────────────────────────────────────────────────────────┐
│  Memory updated                                              │
├─────────────────────────────────────────────────────────────┤
│  Added to decisions.md:                                      │
│  "Use feature-based structure for new modules"               │
│                                                              │
│  Total: 15 decisions, 8 lessons, 12 knowledge fragments      │
└─────────────────────────────────────────────────────────────┘
```
