# Costs

View token usage and cost estimates.

## Arguments

- `$ARGUMENTS` - "today", "week", "month", or specific date (YYYY-MM-DD)

## Instructions

### Today's Usage

```bash
cat .claude/metrics/daily/$(date +%Y-%m-%d).json 2>/dev/null || echo "No usage data for today"
```

### Weekly Summary

Read last 7 daily files and aggregate:

```bash
# List recent daily files
ls -la .claude/metrics/daily/*.json 2>/dev/null | tail -7
```

Parse each file and sum:
- Total sessions
- Command counts
- Days active

### Monthly Report

Read all daily files for current month:

```bash
# List files for current month
ls .claude/metrics/daily/$(date +%Y-%m)-*.json 2>/dev/null
```

Aggregate:
- Total sessions
- Total commands by type
- Days active
- Average sessions per day

### Specific Date

```bash
cat .claude/metrics/daily/YYYY-MM-DD.json 2>/dev/null
```

## Output

```
┌─────────────────────────────────────────────────────────────┐
│  📊 USAGE REPORT                                            │
├─────────────────────────────────────────────────────────────┤
│  Period: January 2026                                       │
│                                                             │
│  Sessions: 45                                               │
│  Days Active: 15                                            │
│                                                             │
│  Top Commands:                                              │
│  • /ship: 12                                                │
│  • /plan: 18                                                │
│  • /review: 15                                              │
│  • /verify: 12                                              │
│  • /commit: 10                                              │
│                                                             │
│  Average Sessions/Day: 3.0                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Location

Usage data is stored in:
```
.claude/metrics/
├── daily/
│   ├── 2026-01-15.json
│   ├── 2026-01-16.json
│   └── ...
└── usage_summary.json
```

## Daily File Format

```json
{
  "date": "2026-01-20",
  "sessions": [
    {
      "session_id": "abc123",
      "timestamp": "2026-01-20T10:15:00Z",
      "commands": ["/plan", "/implement", "/verify"],
      "duration_seconds": 1800
    }
  ],
  "totals": {}
}
```

## Usage Examples

```bash
# Today's usage
/costs today

# This week
/costs week

# This month
/costs month

# Specific date
/costs 2026-01-15
```

## Notes

- Data is collected automatically via the cost_tracker hook
- No actual API costs are tracked (Claude Code doesn't expose this)
- Useful for understanding usage patterns
- Data is local only, not sent anywhere
