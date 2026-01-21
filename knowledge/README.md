# Knowledge Base

Condensed learnings from YouTube transcripts, articles, and other sources. Used by the `workshop-prep` agent to create company training materials.

## Structure

```
knowledge/
├── ai-development/    # General AI-assisted development topics
├── claude/            # Claude, Anthropic, Claude Code, Claude API
├── prompting/         # Prompt engineering, patterns, techniques
├── agents/            # AI agents, multi-agent systems, agentic workflows
├── mcp-servers/       # Model Context Protocol, MCP servers, tools
├── coding-assistants/ # Cursor, Copilot, AI pair programming
├── workflows/         # AI automation, pipelines, processes
└── other/             # Topics not fitting above categories
```

## Adding Content

Use the `/condense` command:

```
/condense <paste YouTube transcript>
```

The `transcript-condenser` agent will:
1. Analyze and categorize the content
2. Extract key topics and insights
3. Create actionable takeaways
4. Flag workshop-relevant material
5. Save to the appropriate category folder

## Using for Workshops

Use the `/workshop` command:

```
/workshop intro        # Introduction to Claude & AI
/workshop claude-code  # Claude Code deep dive for developers
/workshop prompting    # Prompt engineering workshop
/workshop agents       # AI agents & automation
```

The `workshop-prep` agent will analyze all notes and create structured workshop materials.

## Note Format

Each note follows this structure:
- TL;DR summary
- Key topics with explanations
- Techniques & patterns table
- Actionable takeaways
- Memorable quotes
- Workshop relevance notes
- Related topics
