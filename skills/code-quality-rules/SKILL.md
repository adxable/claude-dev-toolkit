---
name: code-quality-rules
description: Design principles and code quality standards that complement automated tooling
configurable: true
---

# Code Quality Rules

Design principles and quality standards that **cannot be automated by linters** - architectural decisions, abstraction quality, and principle adherence.

## What This Skill Covers vs Tooling

| Concern | This Skill | Tooling (ESLint/TSConfig) |
|---------|------------|---------------------------|
| File size limits | ❌ | ✅ `max-lines` |
| Function length | ❌ | ✅ `max-lines-per-function` |
| Cyclomatic complexity | ❌ | ✅ `complexity` |
| No `any` types | ❌ | ✅ `@typescript-eslint/no-explicit-any` |
| **SOLID violations** | ✅ | ❌ |
| **Premature abstraction** | ✅ | ❌ |
| **Wrong abstraction level** | ✅ | ❌ |
| **Code duplication intent** | ✅ | ❌ |
| **Naming quality** | ✅ | ❌ |

**This skill focuses on what requires judgment, not what can be measured.**

---

## Setup Questions

### Question 1: Project Type

```
Header: "Project"
Question: "What type of project is this?"
Options:
  - label: "Product/Application"
    description: "Long-lived codebase, maintainability matters most"
  - label: "Prototype/MVP"
    description: "Speed matters, some shortcuts acceptable"
  - label: "Library/Package"
    description: "API stability, backwards compatibility critical"
  - label: "Script/Tool"
    description: "One-off or infrequently modified"
```

### Question 2: Team Size

```
Header: "Team"
Question: "How many developers work on this codebase?"
Options:
  - label: "Solo"
    description: "You know the full context, less documentation needed"
  - label: "Small team (2-5)"
    description: "Shared context, moderate documentation"
  - label: "Large team (6+)"
    description: "Explicit contracts, clear boundaries essential"
```

### Question 3: Abstraction Philosophy

```
Header: "Abstraction"
Question: "When should code be abstracted?"
Options:
  - label: "Rule of Three (Recommended)"
    description: "Abstract on 3rd use - avoid premature abstraction"
  - label: "DRY Strict"
    description: "Abstract immediately on 2nd occurrence"
  - label: "Minimal"
    description: "Prefer duplication over wrong abstraction"
```

---

## Configuration

```json
{
  "projectType": "product",
  "teamSize": "small",
  "abstractionRule": "rule-of-three",
  "tooling": {
    "eslint": true,
    "typescript": true
  }
}
```

---

## Core Principles

### 1. Single Responsibility (What Linters Can't Check)

Linters count lines. This skill evaluates **cohesion**.

```
ASK: "If I describe what this module does, do I use 'and'?"

BAD: "This service fetches users AND validates input AND formats output"
     → Three responsibilities, should be split

GOOD: "This service manages user data persistence"
      → One clear responsibility
```

**Detection patterns:**
- Module has multiple "reason to change" scenarios
- Class/file name includes "And", "Manager", "Handler", "Utils" (smell, not always bad)
- Imports span multiple domains (UI + API + DB in one file)

**When reviewing:**
```
[quality] Checking UserService.ts...
[quality] ⚠ Multiple responsibilities detected:
  - Lines 1-50: User CRUD operations
  - Lines 51-80: Email validation
  - Lines 81-120: Password hashing
[quality] → Consider: UserRepository, EmailValidator, PasswordService
```

### 2. Abstraction Quality (Not Quantity)

**Wrong abstraction is worse than duplication.**

```typescript
// BAD: Premature abstraction after seeing 2 similar things
const useDataFetcher = (url, transform, onError, retries, cache) => { ... }

// Usage becomes harder than the original:
useDataFetcher('/users', transformUser, handleError, 3, true);
useDataFetcher('/orders', transformOrder, handleError, 3, false);

// GOOD: Wait for 3rd use case, then extract common pattern
// Or accept some duplication if use cases are actually different
```

**Rule of Three checklist:**
```
□ Have I seen this pattern 3+ times?
□ Are the variations predictable, not arbitrary?
□ Would the abstraction be simpler than the duplicated code?
□ Can I name the abstraction clearly without "Generic" or "Common"?
```

### 3. Naming as Documentation

Good names eliminate need for comments.

```typescript
// BAD: Name doesn't reveal intent
const data = await fetch(url);
const result = process(data);
if (check(result)) { ... }

// GOOD: Names are self-documenting
const userProfile = await fetchUserProfile(userId visually);
const validatedProfile = validateRequiredFields(userProfile);
if (hasCompletedOnboarding(validatedProfile)) { ... }
```

**Naming quality checks:**
- [ ] Can a new developer understand without asking?
- [ ] Does the name describe WHAT, not HOW?
- [ ] Is it searchable (not `temp`, `data`, `result`)?
- [ ] Does scope match specificity? (broader scope = more specific name)

### 4. Dependency Direction

High-level modules shouldn't depend on low-level details.

```
┌─────────────────────────────────────────┐
│           Business Logic                │  ← Pure, no I/O
│  (calculateDiscount, validateOrder)     │
├─────────────────────────────────────────┤
│           Application Layer             │  ← Orchestration
│  (CheckoutService, OrderWorkflow)       │
├─────────────────────────────────────────┤
│           Infrastructure                │  ← I/O, external
│  (ApiClient, Database, EmailSender)     │
└─────────────────────────────────────────┘

RULE: Arrows point DOWN only
      Business logic never imports from Infrastructure
```

### 5. Complexity Budget

Every feature has a complexity cost. Spend wisely.

```
BUDGET ANALYSIS:

Feature: Add dark mode toggle

Complexity costs:
- Theme context/store: +1
- CSS variables setup: +1
- Persistence (localStorage): +1
- System preference detection: +1
- Animation on switch: +2 (adds CSS complexity)
- Per-component overrides: +3 (scattered logic)

Total: 9 complexity points

Question: Is dark mode worth 9 points?
- If core feature → Yes, invest
- If nice-to-have → Maybe skip animation/per-component
- If prototype → Skip entirely, add later
```

---

## Required Tooling Configuration

This skill assumes these ESLint/TypeScript rules are enabled:

```javascript
// .eslintrc.js (or eslint.config.js)
module.exports = {
  rules: {
    // Let tooling handle measurable limits
    'max-lines': ['warn', { max: 300, skipBlankLines: true }],
    'max-lines-per-function': ['warn', { max: 50 }],
    'complexity': ['warn', 10],
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'off', // Let inference work

    // Naming
    '@typescript-eslint/naming-convention': [
      'error',
      { selector: 'interface', format: ['PascalCase'] },
      { selector: 'typeAlias', format: ['PascalCase'] },
    ],
  },
};
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**If tooling is not configured**, this skill will suggest adding it rather than manually enforcing measurable rules.

---

## React Memoization (Performance-First)

**CRITICAL: Performance > preventing re-renders. Memoization has a cost.**

This is a design decision linters can't catch. Apply judgment.

### When Memoization Helps

| Pattern | Use ONLY When |
|---------|---------------|
| `memo()` | 50+ list items AND render >1ms AND props are stable |
| `useMemo()` | Computation >1ms (1000+ items filter/sort) |
| `useCallback()` | Passed to working `memo()` child with stable other props |

### When Memoization Hurts (Remove It)

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| `memo()` on propless component | Adds overhead, no props to compare |
| `memo()` with object props | Props are new refs each render, never bails out |
| `useMemo()` for Array.find | find() is ~0.01ms, memo overhead exceeds savings |
| `useCallback()` → DOM element | `<button onClick>` never checks ref equality |
| `useCallback()` → shadcn/radix | These components are NOT memoized |

### Detection Pattern

```
[quality] Checking for memoization anti-patterns...
[quality] ⚠ VesselLibraryLanding.tsx:
  - memo() on component with no props (remove wrapper)
[quality] ⚠ VesselSearchCombobox.tsx:
  - useMemo() for items.find() - operation is <1ms (remove useMemo)
  - useCallback() passed to DOM <span> - never helps (remove useCallback)
[quality] ⚠ AbstractComponentsPanel.tsx:
  - memo() with object props (criteria, data) - will never bail out
  → Consider: Remove memo or ensure stable prop references
```

---

## Review Checklist

When reviewing code, evaluate:

```
┌─────────────────────────────────────────────────────────────┐
│  CODE QUALITY REVIEW                                        │
├─────────────────────────────────────────────────────────────┤
│  Responsibility:                                            │
│  □ Each module has ONE clear purpose                        │
│  □ No "and" in describing what it does                      │
│  □ Changes for one reason only                              │
│                                                             │
│  Abstraction:                                               │
│  □ No premature abstraction (rule of 3)                     │
│  □ Abstractions are simpler than alternatives               │
│  □ Can name it without "Generic/Common/Base"                │
│                                                             │
│  Naming:                                                    │
│  □ Intent is clear from names                               │
│  □ No abbreviations except industry standard                │
│  □ Searchable, not generic                                  │
│                                                             │
│  Dependencies:                                              │
│  □ High-level doesn't import low-level                      │
│  □ No circular dependencies                                 │
│  □ External dependencies isolated                           │
│                                                             │
│  Memoization (React):                                       │
│  □ No memo() on simple/propless components                  │
│  □ No useMemo() for cheap ops (<1ms)                        │
│  □ No useCallback() for DOM handlers                        │
│  □ memo() only with stable props that actually change       │
└─────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns This Skill Catches

| Anti-Pattern | Why Linters Miss It | How Skill Detects |
|--------------|--------------------|--------------------|
| God class | Lines might be under limit | Multiple responsibilities in description |
| Leaky abstraction | Syntactically valid | Caller needs internal knowledge |
| Shotgun surgery | Each file is fine alone | One change touches many files |
| Feature envy | No syntax violation | Method uses another class's data more than its own |
| Primitive obsession | Types are correct | Stringly-typed or numeric magic values |
| Over-memoization | Syntactically correct | memo/useMemo/useCallback with no performance benefit |

---

## Integration

This skill is loaded during:
- `/adx:plan` - Architecture decisions
- `/adx:implement` - Design choices while coding
- `/adx:review` - Quality assessment

It complements, not replaces, automated tooling.
