# Memory

Manage project memory (decisions and lessons).

## Arguments

- `decision "description"` - Add a new decision
- `lesson "description"` - Add a new lesson
- `show` - Show current memory
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

### Show Memory

Display current contents of:
- `.claude/memory/decisions.md`
- `.claude/memory/lessons.md`
- `.claude/context/session_context.json` (patterns)

**Output format:**
```
┌─────────────────────────────────────────────────────────────┐
│  📚 PROJECT MEMORY                                          │
├─────────────────────────────────────────────────────────────┤
│  DECISIONS (5 total)                                        │
│                                                             │
│  Recent:                                                    │
│  • 2026-01-20: Use TanStack Query queryOptions factory      │
│  • 2026-01-18: Feature-based folder structure               │
│  • 2026-01-15: Zustand for UI state only                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  LESSONS (3 total)                                          │
│                                                             │
│  Recent:                                                    │
│  • 2026-01-20: Zustand + useShallow for object selectors    │
│  • 2026-01-17: Check for existing utilities before creating │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  ESTABLISHED PATTERNS                                       │
│                                                             │
│  • dataFetching: TanStack Query with queryOptions           │
│  • stateManagement: Zustand with useShallow                 │
│  • forms: React Hook Form + Zod                             │
│  • styling: Tailwind + cn() helper                          │
└─────────────────────────────────────────────────────────────┘
```

### Skip

Dismiss the memory update prompt without adding anything.

## Data Location

Memory is stored in:
```
.claude/
├── memory/
│   ├── decisions.md    # Architectural decisions
│   └── lessons.md      # Lessons learned
└── context/
    └── session_context.json  # Patterns & blocked patterns
```

## File Formats

### decisions.md

```markdown
# Project Decisions

Architectural and pattern decisions for this project.

## 2026-01-20 - Use TanStack Query queryOptions factory pattern

Context: Implementing data fetching layer
Reason: Provides better type inference and query key organization

## 2026-01-18 - Feature-based folder structure

Context: Initial project setup
Reason: Better scalability as project grows
```

### lessons.md

```markdown
# Lessons Learned

Problems encountered and their solutions.

## 2026-01-20 - Zustand without useShallow causes infinite re-renders

Context: Object selector in Zustand store causing component re-render loop
Solution: Wrapped selector with useShallow from zustand/shallow
Prevention: Always use useShallow when selecting object/array from Zustand
```

## Usage Examples

```bash
# Add a decision
/memory decision "Use Vitest for unit testing"

# Add a lesson
/memory lesson "React 19 requires useOptimistic for optimistic updates"

# Show all memory
/memory show

# Dismiss prompt
/memory skip
```

## Integration

Memory files are automatically read by:
- `context_loader.py` hook (injects into prompts)
- `/plan` command (considers past decisions)
- Code reviewer agent (checks for pattern consistency)

## Output

```
┌─────────────────────────────────────────────────────────────┐
│  ✓ Memory updated                                           │
├─────────────────────────────────────────────────────────────┤
│  Added to decisions.md:                                     │
│  "Use feature-based structure for new modules"              │
│                                                             │
│  Total: 15 decisions, 8 lessons                             │
└─────────────────────────────────────────────────────────────┘
```
