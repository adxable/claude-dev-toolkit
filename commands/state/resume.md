# /adx:resume

Restore context from last session and continue work.

## Trigger

User runs `/adx:resume` at the start of a new session.

## Behavior

1. **Load state files:**
   - Read `.claude/state/STATE.md`
   - Read `.claude/state/ROADMAP.md`
   - Read `.claude/state/PROJECT.md` (if exists)

2. **Display session summary:**

```
## Resuming: [Project Name]

### Last Session (2024-01-20)

**Position:** Phase 2 - User Profile | Task: UserCard styling

**Context:**
Working on UserCard.tsx - avatar added, styling incomplete.
Next step was adding hover states.

**Decisions Made:**
- Use Tailwind aspect-ratio for image sizing

**Blockers:**
- [ ] API doesn't return avatar URL

**Open Questions:**
- [ ] Avatar fallback: initials or generic icon?

### Recommended Next Action
Continue UserCard styling - add hover effect with scale transform

---

Ready to continue. What would you like to work on?
```

3. **Offer options:**
   - Continue where left off
   - Check `/adx:progress` for full status
   - Work on something else

## Important

- **Read all context:** Don't skip the Session Context section
- **Check blockers:** May have been resolved externally
- **Verify decisions:** User may want to revisit

## Edge Cases

- **No previous session:** "No saved state found. Run `/adx:init-state` to set up tracking."
- **State is stale:** Warn if last updated > 7 days ago
- **Blockers resolved:** Prompt to update STATE.md

## Example Output

```
## Resuming: E-Commerce Dashboard

### Last Session (2024-01-19)

**Position:** Phase 3 - Payment Integration | Task: Stripe webhooks

**Context:**
Implementing webhook endpoint at `/api/webhooks/stripe`.
Created handler for `checkout.session.completed` event.
Need to add: `payment_intent.payment_failed` handler.

File: `src/app/api/webhooks/stripe/route.ts`

**Decisions Made:**
- Verify webhook signatures in middleware
- Store payment events in separate table for audit

**Blockers:**
- [ ] Need Stripe webhook secret for local testing

**Open Questions:**
- [ ] Retry failed webhooks or mark as failed?

### Recommended Next Action
Add `payment_intent.payment_failed` handler to webhook endpoint

---

Ready to continue. What would you like to work on?
```
