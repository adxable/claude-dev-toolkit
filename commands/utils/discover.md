# Discover

Research latest Claude Code patterns and suggest toolkit improvements.

## Arguments

- `$ARGUMENTS` - Focus: "hooks", "agents", "workflows", "security", "all"

## Instructions

Use the pattern-researcher agent to research and compare patterns.

### 1. Spawn Pattern Researcher

Use the Task tool to spawn the pattern-researcher agent:

```
Task: "Research Claude Code patterns with focus on {focus area}.
       Search official and community sources.
       Compare with current ADX toolkit.
       Generate recommendations report."
```

### 2. Search Official Sources

The agent will search:
- Anthropic docs and blog
- Claude Code repository
- Official examples

### 3. Search Community Sources

The agent will search:
- awesome-claude-code
- GitHub claude-code topic
- Community toolkits

### 4. Compare with Current Toolkit

The agent will:
- Read current commands/*.md
- Read current agents/*.md
- Read current hooks/*.py
- Identify gaps

### 5. Generate Report

Save report to `.claude/discovery/report-{date}.md`

## Output Format

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 DISCOVERY REPORT                                        │
├─────────────────────────────────────────────────────────────┤
│  Focus: {focus area}                                        │
│  Date: {date}                                               │
│  Sources checked: {N}                                       │
├─────────────────────────────────────────────────────────────┤
│  NEW PATTERNS FOUND                                         │
│                                                             │
│  1. Pattern Name                                            │
│     Source: {url}                                           │
│     In toolkit: No                                          │
│     Should add: Yes                                         │
│     Effort: Low                                             │
│                                                             │
│  2. Pattern Name                                            │
│     Source: {url}                                           │
│     In toolkit: Partial                                     │
│     Should add: Yes (enhance)                               │
│     Effort: Medium                                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  RECOMMENDATIONS                                            │
│                                                             │
│  High Priority:                                             │
│  • Add X (Low effort, high value)                           │
│  • Enhance Y with Z                                         │
│                                                             │
│  Medium Priority:                                           │
│  • Consider adding W                                        │
│                                                             │
│  Low Priority:                                              │
│  • Nice to have: V                                          │
└─────────────────────────────────────────────────────────────┘
```

## Focus Areas

### hooks
Research new hook patterns:
- Event types (UserPromptSubmit, Stop, etc.)
- Data injection techniques
- Error handling patterns

### agents
Research agent patterns:
- Specialized agents
- Agent orchestration
- Tool configurations

### workflows
Research workflow patterns:
- Command sequences
- Automation patterns
- Integration techniques

### security
Research security patterns:
- Secret scanning
- Vulnerability detection
- Safe execution

### all
Comprehensive research across all areas.

## Usage Examples

```bash
# Research all patterns
/discover all

# Focus on hooks
/discover hooks

# Focus on agents
/discover agents

# Focus on workflows
/discover workflows

# Focus on security
/discover security
```

## Report Location

Reports are saved to:
```
.claude/discovery/
├── report-2026-01-20.md
├── report-2026-01-15.md
└── ...
```

## Follow-up Actions

After discovery, you can:
1. Review the report
2. Decide which patterns to adopt
3. Create implementation plans:
   ```
   /plan "Add pattern X from discovery report"
   ```

## Sources

Official:
- https://docs.anthropic.com/en/docs/claude-code
- https://www.anthropic.com/engineering
- https://github.com/anthropics/claude-code

Community:
- https://github.com/hesreallyhim/awesome-claude-code
- https://github.com/topics/claude-code
