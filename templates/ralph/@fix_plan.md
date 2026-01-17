# Development Plan: {{FEATURE_NAME}}

## Priority 1 - Planning & Research

- [ ] Search codebase for similar implementations
- [ ] Identify relevant files and patterns
- [ ] Create implementation plan in `.claude/plans/`
- [ ] Review CLAUDE.md conventions

## Priority 2 - Core Implementation

- [ ] Create feature folder structure (`src/features/{{feature}}/`)
- [ ] Implement main component(s)
- [ ] Add TypeScript types/interfaces
- [ ] Implement hooks (if needed)
- [ ] Add API/query integration (if needed)
- [ ] Add state management (if needed)

## Priority 3 - Quality & Cleanup

- [ ] Run type check (`npx tsc --noEmit`)
- [ ] Fix any type errors
- [ ] Run linter (`npx eslint src/`)
- [ ] Fix any lint issues
- [ ] Remove dead code
- [ ] Remove `any` types
- [ ] Ensure `useShallow` for Zustand selectors

## Priority 4 - Build & Verify

- [ ] Run build (`npm run build`)
- [ ] Fix any build errors
- [ ] Verify feature works as expected
{{BROWSER_TASKS}}

## Priority 5 - Review

- [ ] Run code review (`/review`)
- [ ] Address critical issues
- [ ] Address important issues
- [ ] Run performance audit
- [ ] Run accessibility check (if UI feature)

## Priority 6 - Ship

- [ ] Stage changes
- [ ] Create commit with descriptive message
- [ ] Push to remote
- [ ] Create PR with summary

## Completed

<!-- Move completed items here -->

---

## Notes

<!-- Add any notes, blockers, or decisions here -->

## Errors Encountered

<!-- Track errors and how they were resolved -->

| Error | Resolution | Loop |
|-------|------------|------|
| | | |
