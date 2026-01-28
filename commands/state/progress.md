# /adx:progress

Show current project position and recommend next action.

## Trigger

User runs `/adx:progress` or asks "where am I?" / "what's next?"

## Behavior

1. **Read state files:**
   - `.claude/state/STATE.md` - Current position, blockers
   - `.claude/state/ROADMAP.md` - Phase progress
   - `.claude/state/REQUIREMENTS.md` - Requirement completion

2. **Calculate progress:**
   - Count completed vs total phases
   - Count completed vs total requirements (v1)
   - Identify current phase status

3. **Check for blockers:**
   - List any unchecked items in Blockers section
   - List any unresolved Questions

4. **Output format:**

```
## Project Progress

**Current Position:** Phase 2 of 5 - User Authentication
**Phase Status:** In Progress (3/6 tasks complete)
**Overall Progress:** 28% (v1 requirements)

### Current Task
[Description from STATE.md]

### Blockers
- [ ] Need API credentials from backend team

### Next Actions
1. [Immediate next task from roadmap]
2. [Following task]

### Recent Decisions
- Chose JWT over sessions (2024-01-15)
```

## Edge Cases

- **State not initialized:** Prompt to run `/adx:init-state`
- **No current task:** Suggest starting next phase
- **All phases complete:** Congratulate and suggest `/adx:init-state` for next milestone

## Example Output

```
## Project Progress

**Current Position:** Phase 3 of 4 - Payment Integration
**Phase Status:** In Progress (2/5 tasks complete)
**Overall Progress:** 65% (v1 requirements)

### Current Task
Implementing Stripe checkout flow with webhook handling

### Blockers
None

### Next Actions
1. Complete webhook endpoint for payment confirmation
2. Add error handling for failed payments
3. Write integration tests for payment flow

### Recent Decisions
- Using Stripe over PayPal (broader API support) - 2024-01-20
- Webhook-based confirmation over polling - 2024-01-20
```
