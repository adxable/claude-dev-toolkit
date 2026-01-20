---
name: frontend-dev-guidelines
description: React patterns and best practices - auto-detects your stack from package.json
configurable: true
---

# Frontend Development Guidelines

React patterns and best practices. **Detects your actual stack** from package.json and provides relevant guidance only.

## Stack Detection

Before providing any guidance, detect installed packages:

```
STEP 1: Read package.json dependencies

STEP 2: Identify stack
  State:     zustand | redux | jotai | mobx | context-only
  Server:    @tanstack/react-query | swr | rtk-query | none
  Forms:     react-hook-form | formik | react-final-form | native
  Styling:   tailwindcss | styled-components | emotion | css-modules
  UI:        @radix-ui/* | @mui/* | @chakra-ui/* | none
  Router:    @tanstack/react-router | react-router | next | remix

STEP 3: Output detected stack
  [frontend] Detected stack:
  [frontend] • State: zustand
  [frontend] • Server state: @tanstack/react-query
  [frontend] • Forms: react-hook-form + zod
  [frontend] • Styling: tailwindcss + class-variance-authority
  [frontend] • UI: @radix-ui/* (shadcn/ui pattern)
  [frontend] → Loading relevant patterns only
```

**No assumptions. Only enforce patterns for installed packages.**

---

## Setup Questions

### Question 1: Confirm Detection

```
Header: "Stack"
Question: "I detected: [stack summary]. Correct?"
Options:
  - label: "Yes, use these patterns"
    description: "Load guidelines for detected libraries"
  - label: "Missing something"
    description: "I'll add libraries that aren't in package.json yet"
  - label: "Planning to migrate"
    description: "Show patterns for library I'm migrating to"
```

### Question 2: Strictness

```
Header: "Strictness"
Question: "How strictly should patterns be enforced?"
Options:
  - label: "Strict (Recommended)"
    description: "Flag all deviations from best practices"
  - label: "Moderate"
    description: "Flag critical issues, warn on others"
  - label: "Relaxed"
    description: "Suggestions only, no enforcement"
```

---

## Stack-Specific Patterns

### IF: Zustand Detected

```typescript
// CRITICAL: Always use useShallow for object selectors
// Without it: infinite re-render loop

// ❌ CAUSES INFINITE LOOP
const { user, setUser } = useUserStore((state) => ({
  user: state.user,
  setUser: state.setUser,
}));

// ✅ CORRECT
import { useShallow } from 'zustand/shallow';

const { user, setUser } = useUserStore(
  useShallow((state) => ({
    user: state.user,
    setUser: state.setUser,
  }))
);

// ✅ ALSO CORRECT: Single primitive selector (no useShallow needed)
const user = useUserStore((state) => state.user);
```

**Store pattern:**
```typescript
import { create } from 'zustand';

interface UserStore {
  // State
  user: User | null;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  reset: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  isLoading: false,

  setUser: (user) => set({ user }),
  reset: () => set({ user: null, isLoading: false }),
}));
```

---

### IF: TanStack Query Detected

```typescript
// PATTERN: Query Options Factory
// Centralizes query configuration, enables type inference

// queries.ts
import { queryOptions } from '@tanstack/react-query';

export const userQueries = {
  all: () => queryOptions({
    queryKey: ['users'],
    queryFn: fetchUsers,
  }),

  detail: (id: string) => queryOptions({
    queryKey: ['users', id],
    queryFn: () => fetchUser(id),
  }),

  list: (filters: Filters) => queryOptions({
    queryKey: ['users', 'list', filters],
    queryFn: () => fetchUsers(filters),
  }),
};

// Usage
const { data } = useSuspenseQuery(userQueries.detail(userId));
```

**Suspense pattern:**
```typescript
// Wrap with Suspense at layout level, NOT per-query
function UsersPage() {
  return (
    <Suspense fallback={<Skeleton />}>
      <UserList />
    </Suspense>
  );
}

function UserList() {
  // useSuspenseQuery - no loading state needed in component
  const { data: users } = useSuspenseQuery(userQueries.all());
  return users.map(user => <UserCard key={user.id} user={user} />);
}
```

---

### IF: SWR Detected

```typescript
// Pattern: SWR with global config
import useSWR from 'swr';

// Configure fetcher globally
const fetcher = (url: string) => fetch(url).then(res => res.json());

// Usage
function UserProfile({ id }: { id: string }) {
  const { data, error, isLoading } = useSWR(`/api/users/${id}`, fetcher);

  if (error) return <ErrorDisplay error={error} />;
  if (isLoading) return <Skeleton />;
  return <Profile user={data} />;
}
```

---

### IF: React Hook Form + Zod Detected

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema FIRST
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

// Infer type FROM schema
type FormData = z.infer<typeof schema>;

// Form setup
function LoginForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { email: '', password: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('email')} />
      {form.formState.errors.email && (
        <span>{form.formState.errors.email.message}</span>
      )}
      {/* ... */}
    </form>
  );
}
```

---

### IF: Formik Detected

```typescript
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const schema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(8, 'Min 8 characters').required('Required'),
});

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={schema}
      onSubmit={handleSubmit}
    >
      <Form>
        <Field name="email" type="email" />
        <ErrorMessage name="email" component="span" />
        {/* ... */}
      </Form>
    </Formik>
  );
}
```

---

### IF: Tailwind Detected

```typescript
// REQUIRED: Use cn() helper for conditional classes
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<div className={cn(
  'rounded-lg border p-4',
  isActive && 'border-blue-500 bg-blue-50',
  disabled && 'opacity-50 cursor-not-allowed',
  className // Allow prop override
)} />
```

**IF: class-variance-authority (cva) also detected:**
```typescript
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-white hover:bg-primary/90',
        outline: 'border border-input bg-transparent hover:bg-accent',
      },
      size: {
        default: 'h-10 px-4',
        sm: 'h-8 px-3 text-sm',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  // ...
}
```

---

### IF: Redux Toolkit Detected

```typescript
// Slice pattern
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  user: User | null;
  status: 'idle' | 'loading' | 'failed';
}

const initialState: UserState = { user: null, status: 'idle' };

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
  },
});

// Typed hooks
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

---

## Universal React Patterns

These apply regardless of stack:

### 1. Memoization

```typescript
// useMemo: Expensive calculations
const sorted = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// useCallback: Functions passed to memoized children
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// React.memo: List item components
export const ListItem = memo(function ListItem({ item }: Props) {
  return <div>{item.name}</div>;
});
```

### 2. Keys

```typescript
// ❌ NEVER: Index as key
{items.map((item, index) => <Item key={index} {...item} />)}

// ✅ ALWAYS: Stable unique identifier
{items.map(item => <Item key={item.id} {...item} />)}
```

### 3. Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Usage at layout level
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <App />
</ErrorBoundary>
```

### 4. Named Exports

```typescript
// ✅ PREFERRED: Named exports
export const UserCard = () => { ... };
export function useUsers() { ... }

// ❌ AVOID: Default exports (harder to refactor, worse tree-shaking)
export default UserCard;
```

---

## Configuration

```json
{
  "detected": {
    "state": "zustand",
    "serverState": "tanstack-query",
    "forms": "react-hook-form",
    "validation": "zod",
    "styling": "tailwindcss",
    "ui": "radix-ui"
  },
  "strictness": "strict",
  "patterns": {
    "useShallow": true,
    "queryOptionsFactory": true,
    "cnHelper": true,
    "namedExports": true
  }
}
```

---

## Validation by Detected Stack

| If Detected | Check | Severity |
|-------------|-------|----------|
| zustand | `useShallow` for object selectors | Error |
| @tanstack/react-query | `queryOptions()` factory pattern | Warning |
| @tanstack/react-query | `useSuspenseQuery` + Suspense wrapper | Warning |
| react-hook-form + zod | `zodResolver` in useForm | Warning |
| tailwindcss | `cn()` for conditional classes | Warning |
| Any | Index as list key | Error |
| Any | Default exports in components | Info |

---

## What This Skill Does NOT Cover

| Concern | Handle With |
|---------|-------------|
| Bundle size limits | Build tooling (webpack-bundle-analyzer) |
| Lighthouse scores | CI performance testing |
| Accessibility | axe-core, eslint-plugin-jsx-a11y |
| Type safety | TypeScript strict mode |
| Code formatting | Prettier |

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND CHECKLIST (stack-dependent)                       │
├─────────────────────────────────────────────────────────────┤
│  IF Zustand:                                                │
│  □ useShallow for object/array selectors                    │
│                                                             │
│  IF TanStack Query:                                         │
│  □ queryOptions() factory in api/queries.ts                 │
│  □ Suspense boundary at layout level                        │
│                                                             │
│  IF React Hook Form + Zod:                                  │
│  □ zodResolver in useForm config                            │
│  □ Type inferred from schema (z.infer)                      │
│                                                             │
│  IF Tailwind:                                               │
│  □ cn() helper for conditional classes                      │
│                                                             │
│  ALWAYS:                                                    │
│  □ Stable keys in lists (never index)                       │
│  □ React.memo for list item components                      │
│  □ Named exports (no default)                               │
│  □ Error boundary at app/layout level                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration

Loaded during:
- `/adx:plan` - Suggests patterns based on detected stack
- `/adx:implement` - Applies stack-specific patterns
- `/adx:review` - Validates against detected stack only

**Only enforces rules for packages that exist in your project.**
