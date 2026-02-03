# Project Conventions

> Critical patterns enforced in all React/TypeScript projects.

## Abstraction Rules

### Rule of Three
Abstract only after seeing a pattern 3+ times. Premature abstraction is worse than duplication.

```
Before abstracting, ask:
- Have I seen this pattern 3+ times?
- Are the variations predictable, not arbitrary?
- Would the abstraction be simpler than duplicated code?
- Can I name it clearly without "Generic" or "Common"?
```

## Component Patterns

### No Early Returns for Loading States

```tsx
// BAD - causes layout shift
if (isLoading) {
  return <Spinner />;
}

// GOOD - use Suspense or overlay
<Suspense fallback={<Spinner />}>
  <Content />
</Suspense>
```

### Memoization: Only When Measured

| Pattern | Use ONLY When |
|---------|---------------|
| `memo()` | 50+ list items AND render >1ms AND props are stable |
| `useMemo()` | Computation >1ms (1000+ items filter/sort) |
| `useCallback()` | Passed to working `memo()` child |

**Remove memoization if:**
- Component has no props or simple primitive props
- Props are new object references each render
- Passed to DOM elements (`<button onClick>`)
- Operation is cheap (<1ms)

## Async Patterns

### Parallel Fetching (Critical)

```tsx
// BAD - waterfall
const users = await fetchUsers();
const orders = await fetchOrders();

// GOOD - parallel
const [users, orders] = await Promise.all([
  fetchUsers(),
  fetchOrders()
]);
```

### Defer Await

```tsx
// BAD - awaits even when not needed
async function getUser(id: string, options?: { includeOrders: boolean }) {
  const user = await fetchUser(id);
  const orders = await fetchOrders(id);  // Always awaited

  if (options?.includeOrders) {
    return { ...user, orders };
  }
  return user;
}

// GOOD - await only in branch where needed
async function getUser(id: string, options?: { includeOrders: boolean }) {
  const user = await fetchUser(id);

  if (options?.includeOrders) {
    const orders = await fetchOrders(id);  // Only when needed
    return { ...user, orders };
  }
  return user;
}
```

## Module Boundaries

### Features Don't Import Features

```tsx
// BAD - cross-feature import
// src/features/orders/OrderSummary.tsx
import { UserAvatar } from '@/features/users/components/UserAvatar';

// GOOD - import from shared or compose at route level
import { Avatar } from '@/components/ui/Avatar';
```

### Dependency Direction

```
Routes/Pages     → can import everything
Features         → can import shared, lib
Shared/Components → can import lib only
Lib/Utils        → can import external packages only
```

## TypeScript

### No `any`

```tsx
// BAD
const data: any = response.json();

// GOOD
const data: unknown = await response.json();
const parsed = schema.parse(data);  // Validate with Zod/etc
```

### Prefer `unknown` + Type Guard

```tsx
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}
```

## Naming

| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Hook | useCamelCase | `useUserData.ts` |
| Utility | camelCase | `formatDate.ts` |
| Constant | UPPER_SNAKE | `API_BASE_URL` |
| Type/Interface | PascalCase | `UserData` |

## Import Order

1. React / external libraries
2. Internal modules (`@/`)
3. Relative imports
4. Types (`import type`)
5. Styles
