---
name: workshop
description: Prepare company workshop materials from knowledge base
user_invocable: true
---

# /workshop - Workshop Preparation

Analyze the knowledge base and create workshop materials for company training.

## Usage

```
/workshop intro          # Introduction to Claude & AI
/workshop claude-code    # Claude Code deep dive
/workshop prompting      # Prompt engineering workshop
/workshop agents         # AI agents & automation
/workshop <custom topic> # Custom workshop on specific topic
```

## Process

1. Use the `workshop-prep` agent
2. Agent will:
   - Scan all notes in `knowledge/` folder
   - Identify relevant content for the workshop type
   - Synthesize themes and patterns
   - Create structured workshop outline
   - Generate speaker notes and exercises
   - Build participant materials

## Workshop Types

| Command | Audience | Duration |
|---------|----------|----------|
| `intro` | Entire company | 2-3 hours |
| `claude-code` | Developers | Half day |
| `prompting` | All roles | 2 hours |
| `agents` | Technical teams | Half day |
| `<topic>` | Specified | Variable |

## Output Location

Workshop materials are saved to:
```
workshops/{workshop-name}/
├── outline.md           # Full agenda
├── speaker-notes.md     # Talking points & demos
├── participant-guide.md # Exercises & references
├── slides-outline.md    # Slide suggestions
└── exercises/           # Exercise files
```

## Prerequisites

Build up your knowledge base first using `/condense` to add learning notes from YouTube transcripts, articles, and other sources.

## Agent

Uses: `workshop-prep` (opus)
