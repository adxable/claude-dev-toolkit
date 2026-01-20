---
name: project-structure
description: Folder organization and module boundaries - detects existing patterns, adapts to your framework
configurable: true
---

# Project Structure

Establishes and maintains consistent folder organization. **Detects your existing structure first**, then enforces consistency.

## Philosophy

1. **Detect, don't dictate** - Analyze existing patterns before suggesting changes
2. **Consistency over preference** - Any consistent pattern beats a "perfect" inconsistent one
3. **Framework-aware** - Next.js, Remix, Vite, etc. have different conventions

---

## Auto-Detection

Before applying any rules, detect:

```
1. FRAMEWORK DETECTION
   □ package.json dependencies → next, remix, vite, cra, etc.
   □ Config files → next.config.js, vite.config.ts, remix.config.js
   □ Folder structure → app/ (Next 13+), pages/ (Next 12), routes/ (Remix)

2. EXISTING PATTERN DETECTION
   □ Scan src/ or app/ for organization style
   □ Count: features/, modules/, domains/ → Feature-based
   □ Count: components/, hooks/, services/ at root → Layer-based
   □ Count: (group)/ folders in app/ → Next.js route groups

3. NAMING CONVENTION DETECTION
   □ Sample 20 component files
   □ Majority PascalCase? kebab-case? camelCase?
   □ Detect suffix patterns: .component.tsx, .hook.ts, etc.

4. EXPORT STYLE DETECTION
   □ Sample index.ts files
   □ Barrel exports present? Consistent usage?
```

**Output detection results before suggesting changes:**

```
[structure] Detected framework: Next.js 14 (App Router)
[structure] Organization: Hybrid (app/ for routes, src/features/ for logic)
[structure] Naming: PascalCase components, camelCase hooks
[structure] Exports: Barrel exports at feature level
[structure] → Will enforce existing patterns for consistency
```

---

## Setup Questions

### Question 1: Detection Confirmation

```
Header: "Detected"
Question: "I detected [X pattern]. Is this correct?"
Options:
  - label: "Yes, enforce this pattern"
    description: "Maintain consistency with existing structure"
  - label: "No, I want to change it"
    description: "I'll specify the desired pattern"
  - label: "It's inconsistent, help me fix it"
    description: "Analyze and suggest consolidation"
```

### Question 2: If New Project or Changing

```
Header: "Architecture"
Question: "How should code be organized?"
Options:
  - label: "Feature-based (Recommended)"
    description: "features/users/{components,hooks,api} - scales well"
  - label: "Layer-based"
    description: "components/, hooks/, services/ at root - simpler for small projects"
  - label: "Framework default"
    description: "Follow Next.js/Remix/etc conventions exactly"
```

### Question 3: Colocation Preference

```
Header: "Colocation"
Question: "Should related files live together?"
Options:
  - label: "Colocate everything (Recommended)"
    description: "Component + test + styles in same folder"
  - label: "Separate test folder"
    description: "__tests__/ mirrors src/ structure"
  - label: "Framework convention"
    description: "Follow whatever the framework suggests"
```

---

## Framework-Specific Structures

### Next.js 13+ (App Router)

```
app/                          # Routes (framework-controlled)
├── (marketing)/              # Route group
│   ├── page.tsx
│   └── layout.tsx
├── (dashboard)/
│   ├── users/
│   │   ├── page.tsx
│   │   └── [id]/
│   │       └── page.tsx
│   └── layout.tsx
├── api/                      # API routes
│   └── users/
│       └── route.ts
└── layout.tsx

src/                          # Application code (your control)
├── features/                 # Business logic
│   └── users/
│       ├── components/
│       ├── hooks/
│       ├── actions/          # Server actions
│       └── queries/          # Data fetching
├── components/               # Shared UI
└── lib/                      # Utilities
```

**Key rules:**
- `app/` is for routing only - minimal logic
- Business logic lives in `src/features/`
- Server components are default, mark client explicitly

### Next.js 12 (Pages Router)

```
pages/                        # Routes
├── api/
├── users/
│   ├── index.tsx
│   └── [id].tsx
└── _app.tsx

src/
├── features/
├── components/
└── lib/
```

### Remix

```
app/
├── routes/                   # File-based routing
│   ├── _index.tsx
│   ├── users._index.tsx
│   └── users.$id.tsx
├── components/               # Remix convention: in app/
├── utils/
└── root.tsx
```

### Vite + React (SPA)

```
src/
├── features/
│   └── users/
│       ├── components/
│       ├── hooks/
│       ├── api/
│       └── index.ts
├── components/
├── hooks/
├── lib/
├── routes/                   # TanStack Router or React Router
└── App.tsx
```

---

## Module Boundary Rules

### Rule 1: Features Don't Import Features

```typescript
// ❌ BAD: Cross-feature import
// src/features/orders/OrderSummary.tsx
import { UserAvatar } from '@/features/users/components/UserAvatar';

// ✅ GOOD: Import from shared
import { Avatar } from '@/components/ui/Avatar';

// ✅ GOOD: Compose at route level
// app/orders/page.tsx
import { OrderSummary } from '@/features/orders';
import { UserBadge } from '@/features/users';

export default function OrdersPage() {
  return (
    <OrderSummary
      userSlot={<UserBadge userId={order.userId} />}
    />
  );
}
```

### Rule 2: Dependency Layers

```
┌─────────────────────────────────────────┐
│  Routes/Pages (app/, pages/, routes/)   │
│  Can import: everything                 │
├─────────────────────────────────────────┤
│  Features (src/features/)               │
│  Can import: shared, lib                │
│  Cannot import: other features, routes  │
├─────────────────────────────────────────┤
│  Shared (src/components/, src/hooks/)   │
│  Can import: lib only                   │
├─────────────────────────────────────────┤
│  Lib (src/lib/)                         │
│  Can import: external packages only     │
└─────────────────────────────────────────┘
```

### Rule 3: Public API via index.ts

```typescript
// src/features/users/index.ts
// This is the ONLY entry point for the users feature

// Components (selective export)
export { UserCard } from './components/UserCard';
export { UserList } from './components/UserList';

// Hooks
export { useUsers, useUser } from './hooks/useUsers';

// Types
export type { User, UserFilters } from './types';

// DO NOT export internal utilities, helpers, or implementation details
```

---

## Naming Conventions

### Detection-First Approach

```
STEP 1: Sample existing files
STEP 2: Determine majority pattern
STEP 3: Enforce majority, flag outliers

Example detection:
  UserCard.tsx      → PascalCase
  OrderList.tsx     → PascalCase
  product-card.tsx  → kebab-case (OUTLIER)
  useUsers.ts       → camelCase

Result: Enforce PascalCase for components
Flag: product-card.tsx should be ProductCard.tsx
```

### Conventions by Type

| Type | Convention | Suffix | Example |
|------|------------|--------|---------|
| Components | Match detected | `.tsx` | `UserCard.tsx` |
| Hooks | `use` prefix | `.ts` | `useUsers.ts` |
| Utilities | camelCase | `.ts` | `formatDate.ts` |
| Types | PascalCase | `.ts` | `User.ts` or in `types/index.ts` |
| Constants | UPPER_SNAKE | `.ts` | `API_ENDPOINTS.ts` |
| Tests | Match source | `.test.tsx` | `UserCard.test.tsx` |

---

## Configuration

```json
{
  "detected": {
    "framework": "nextjs-14-app",
    "organization": "feature-based",
    "naming": "pascalcase-components",
    "exports": "feature-barrel"
  },
  "enforced": {
    "organization": "feature-based",
    "naming": "pascalcase-components",
    "exports": "feature-barrel",
    "colocation": true
  },
  "paths": {
    "features": "src/features",
    "shared": "src/components",
    "lib": "src/lib",
    "routes": "app"
  },
  "boundaries": {
    "noFeatureCrossImports": true,
    "maxRelativeDepth": 2
  }
}
```

---

## Validation

### On File Creation

```
[structure] Creating: OrderConfirmation component

[structure] Analyzing context...
[structure] → Related to: orders feature
[structure] → Suggested path: src/features/orders/components/OrderConfirmation.tsx

[structure] Checking conventions...
[structure] ✓ Naming: PascalCase (matches project)
[structure] ✓ Location: feature/components/ (matches pattern)
[structure] ✓ Export: Will add to features/orders/index.ts
```

### On Import

```
[structure] Checking import in src/features/orders/OrderSummary.tsx

[structure] ❌ Invalid: import from '@/features/users/...'
[structure] → Cross-feature import detected
[structure] → Options:
    1. Move UserAvatar to shared: src/components/UserAvatar.tsx
    2. Use slot pattern: pass as prop from route level
    3. Create shared abstraction if truly common
```

---

## Migration Helper

When existing structure is inconsistent:

```
[structure] Inconsistency detected:
  - 60% feature-based (src/features/*)
  - 40% layer-based (src/components/*, src/hooks/*)

[structure] Recommendation: Consolidate to feature-based

[structure] Migration plan:
  1. Move src/components/UserCard.tsx → src/features/users/components/
  2. Move src/hooks/useUsers.ts → src/features/users/hooks/
  3. Update imports (12 files affected)
  4. Keep src/components/ for truly shared UI only

Would you like me to generate a migration script?
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  STRUCTURE CHECKLIST                                        │
├─────────────────────────────────────────────────────────────┤
│  Before creating files:                                     │
│  □ Which feature does this belong to?                       │
│  □ Is it shared across features? → src/components/          │
│  □ Is it feature-specific? → src/features/{name}/           │
│                                                             │
│  Imports:                                                   │
│  □ No cross-feature imports                                 │
│  □ Using @/ aliases (not ../../../)                         │
│  □ Importing from index.ts, not internal files              │
│                                                             │
│  Naming:                                                    │
│  □ Matches detected project convention                      │
│  □ Test file colocated with source                          │
│  □ Exported from feature's index.ts                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration

Loaded during:
- `/adx:plan` - Determines file locations
- `/adx:implement` - Creates files in correct locations
- `/adx:review` - Validates structure consistency

Works with any framework by detecting conventions first.
