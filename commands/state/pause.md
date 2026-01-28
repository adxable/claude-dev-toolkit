# /adx:pause

Save current session state for seamless continuation later.

## Trigger

User runs `/adx:pause` before ending a session.

## Behavior

1. **Gather current context:**
   - What was being worked on?
   - What's partially complete?
   - What decisions were made?
   - What blockers were discovered?

2. **Update STATE.md:**

```markdown
## Position

- **Current Phase:** [Extract from conversation]
- **Current Task:** [What was actively being worked on]
- **Last Updated:** [Current ISO timestamp]

## Session Context

[Detailed description of work in progress, including:
- Files being modified
- Partial implementations
- Next steps that were planned
- Any debugging context]

## Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| [New decisions from this session] | [Why] | [Today] |

## Blockers

- [ ] [Any blockers discovered]

## Questions to Resolve

- [ ] [Open questions that came up]
```

3. **Update ROADMAP.md:**
   - Check off completed tasks
   - Update phase status if changed

4. **Confirm save:**
```
Session state saved to .claude/state/STATE.md

**Captured:**
- Current task: [task description]
- Decisions: [count] new
- Blockers: [count] identified

Run `/adx:resume` in your next session to continue.
```

## Important

- **Be specific:** Include file paths, function names, line numbers
- **Capture intent:** What was the goal, not just what was done
- **Note partial work:** Especially important for incomplete implementations

## Example

**Before pause:**
```
Working on UserCard component, added avatar but styling incomplete.
Decided to use Tailwind aspect-ratio for image sizing.
Blocked on missing user avatar URL from API.
```

**STATE.md after pause:**
```markdown
## Position

- **Current Phase:** Phase 2 - User Profile
- **Current Task:** UserCard component styling
- **Last Updated:** 2024-01-20T15:30:00Z

## Session Context

Working on `src/features/users/components/UserCard.tsx`:
- Added avatar image with aspect-ratio wrapper (line 24-32)
- Styling incomplete - needs hover states and responsive sizing
- Next: Add hover effect with scale transform

## Decisions Made

| Decision | Rationale | Date |
|----------|-----------|------|
| Use Tailwind aspect-ratio | Native support, no extra deps | 2024-01-20 |

## Blockers

- [ ] API doesn't return avatar URL - need backend update

## Questions to Resolve

- [ ] Should avatar have fallback initials or generic icon?
```
