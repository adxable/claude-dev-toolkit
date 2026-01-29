# Memory System

This directory contains project context that Claude Code uses to maintain continuity across sessions.

## Three-Layer Architecture

### L1 - Always Loaded (Static Context)

These files are loaded on every session start:

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Main context file - project overview, stack, conventions | When project setup changes |
| `decisions.md` | Architecture Decision Records (ADRs) | When making significant decisions |
| `conventions.md` | Discovered code patterns and conventions | When patterns are established |
| `lessons.md` | What worked/didn't work, insights | After completing features or fixing issues |

### L2 - Semantic Knowledge Store (Shared)

`memory/knowledge/` - committed to git, shared across the team.

Instead of loading everything, fragments are retrieved by **semantic relevance** to the current prompt using TF-IDF scoring. Only the top 5 most relevant fragments are injected as context.

```
knowledge/
├── index.json         # TF-IDF index of all fragments
└── fragments/         # Individual knowledge fragments
    ├── {id}.json      # Each: content, tags, metadata
    └── ...
```

### L3 - Personal Knowledge (Local)

`memory/local/` - gitignored, per-developer.

Stores personal session context, workflow preferences, and learnings that haven't been promoted to shared yet.

```
local/
├── index.json         # Personal knowledge index
└── fragments/         # Personal fragments
    └── ...
```

## How It Works

### Automatic Retrieval (every prompt)

The `knowledge_loader.py` hook runs on `UserPromptSubmit`:
1. Tokenizes the user's prompt
2. Scores all indexed fragments using TF-IDF
3. Applies tag boosting and recency weighting
4. Shared fragments rank slightly higher than personal
5. Returns top 5 fragments as formatted context

### Automatic Ingestion (session end)

The `knowledge_ingestor.py` hook runs on `Stop`:
1. Parses the session transcript
2. Extracts decisions, error resolutions, and patterns used
3. Creates knowledge fragments with appropriate tags and scope
4. Deduplicates against existing fragments (Jaccard similarity)

### Manual Management

Use `/memory` commands:
- `/memory add "content" --tags tag1,tag2` - add a fragment
- `/memory search "query"` - search the knowledge store
- `/memory show` - view memory status and stats
- `/memory sync` - rebuild index from fragment files
- `/memory promote {id}` - move personal fragment to shared

## Fragment Format

```json
{
  "id": "abc123def456",
  "content": "Use JWT with short-lived tokens for API auth",
  "tags": ["decision", "authentication", "api"],
  "source": "session:abc123",
  "scope": "shared",
  "created": "2025-01-23T10:00:00Z",
  "accessed_count": 3,
  "last_accessed": "2025-01-25T14:30:00Z"
}
```

## Team / Multi-Developer Design

- `memory/knowledge/` is **committed** = shared knowledge (all devs see same fragments)
- `memory/local/` is **gitignored** = personal knowledge (per-developer)
- Retriever queries both stores, merges with shared > personal priority
- `/memory promote` moves a personal fragment to shared (committed via git)
- No external services, databases, or APIs required - pure file-based

## Usage

### For Plugin Users

1. Copy this `memory/` directory to your project's `.claude/memory/`
2. Fill in `CLAUDE.md` with your project specifics
3. Update other files as your project evolves
4. Knowledge fragments build up automatically through sessions

### Auto-Loading

The `CLAUDE.md` file should be placed at:
- Project root: `CLAUDE.md`
- Or: `.claude/CLAUDE.md`
- Or: `.claude/memory/CLAUDE.md`

Claude Code automatically reads `CLAUDE.md` from the project root.

### Best Practices

1. **Keep CLAUDE.md concise** - Focus on what Claude needs to know
2. **Log decisions promptly** - Don't let context get lost
3. **Update lessons regularly** - Capture insights while fresh
4. **Review periodically** - Remove outdated information
5. **Tag fragments well** - Better tags = better retrieval
6. **Promote useful personal fragments** - Share knowledge with the team

## Integration with Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `knowledge_loader.py` | UserPromptSubmit | Retrieves relevant fragments for current prompt |
| `knowledge_ingestor.py` | Stop | Extracts and stores learnings from session |
| `context_loader.py` | UserPromptSubmit | Injects session context (complementary) |
| `memory_updater.py` | Stop | Updates memory files (complementary) |
| `stop.py` | Stop | Session summary (complementary) |
