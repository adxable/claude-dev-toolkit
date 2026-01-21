---
name: condense
description: Condense a YouTube transcript into key learnings
user_invocable: true
---

# /condense - Transcript Condenser

Condense a YouTube transcript into key learnings and store in the knowledge base.

## Usage

```
/condense <transcript or URL>
/condense (then paste transcript)
```

## Process

1. Use the `transcript-condenser` agent
2. Agent will:
   - Analyze the transcript content
   - Categorize it (claude, prompting, agents, etc.)
   - Extract key topics and insights
   - Create actionable takeaways
   - Flag workshop-relevant content
   - Save to `knowledge/{category}/{title}.md`

## Examples

```
/condense https://youtube.com/watch?v=xyz
```

```
/condense
[paste transcript here]
```

## Output Location

Condensed notes are saved to:
```
knowledge/
├── ai-development/
├── claude/
├── prompting/
├── agents/
├── mcp-servers/
├── coding-assistants/
├── workflows/
└── other/
```

## Agent

Uses: `transcript-condenser` (sonnet)
