# Frontend Development Conventions

## Tech Stack

| Category | Choice | Notes |
|----------|--------|-------|
| Router | TanStack Router / React Router v7 | TanStack preferred for new projects |
| State | Zustand | UI state only, NOT server state |
| Server State | TanStack Query | `useSuspenseQuery` with Suspense boundaries |
| Forms | React Hook Form + Zod | Always use `zodResolver` |
| Styling | Tailwind + shadcn/ui | `cn()` from `@/lib/utils` |
| Validation | Zod | Schema-first, `z.infer<>` for types |

---

## Project Structure (Feature-based)

```
src/
├── features/
│   └── users/
│       ├── components/
│       │   ├── UserList.tsx
│       │   └── UserCard.tsx
│       ├── hooks/
│       │   └── useUsers.ts
│       ├── api/
│       │   ├── queries.ts      # TanStack Query options
│       │   └── mutations.ts
│       ├── stores/
│       │   └── userFiltersStore.ts
│       ├── schemas/
│       │   └── userSchema.ts   # Zod schemas
│       └── index.ts            # Public exports
├── components/                  # Shared/global components
├── hooks/                       # Shared hooks
├── lib/
│   └── utils.ts                # cn() helper
└── types/                       # Global types
```

---

## Enforced Patterns

### Zustand - ALWAYS use useShallow

```typescript
// GOOD
import { useShallow } from 'zustand/shallow';

const { filters, setFilter } = useFiltersStore(
  useShallow((state) => ({
    filters: state.filters,
    setFilter: state.setFilter,
  }))
);

// BAD - causes infinite re-render loop
const { filters, setFilter } = useFiltersStore((state) => ({
  filters: state.filters,
  setFilter: state.setFilter,
}));
```

### TanStack Query - Query Options Factory

```typescript
// features/users/api/queries.ts
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
  list: (filters: UserFilters) => queryOptions({
    queryKey: ['users', 'list', filters],
    queryFn: () => fetchUsers(filters),
  }),
};

// Usage
const { data } = useSuspenseQuery(userQueries.detail(userId));
```

### Forms - React Hook Form + Zod

```typescript
// ALWAYS use this pattern
const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email(),
});

type FormData = z.infer<typeof schema>;

const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
});
```

### Tailwind - cn() for conditional classes

```typescript
// ALWAYS use cn() from @/lib/utils
import { cn } from '@/lib/utils';

<div className={cn(
  'rounded-lg p-4',
  isActive && 'bg-primary text-primary-foreground',
  disabled && 'opacity-50 pointer-events-none'
)} />
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `UserCard.tsx` |
| Hooks | camelCase, `use` prefix | `useUsers.ts` |
| Stores | camelCase, `Store` suffix | `userFiltersStore.ts` |
| Schemas | camelCase, `Schema` suffix | `userSchema.ts` |
| Query keys | `['entity', 'action', params]` | `['users', 'list', { page: 1 }]` |

---

## Exports

```typescript
// GOOD - named exports
export const UserCard = () => { ... };
export const useUsers = () => { ... };

// BAD - default exports (harder to refactor)
export default UserCard;
```

---

## Performance - Required

1. **useMemo** for filter/sort/map operations
2. **useCallback** for functions passed to children
3. **React.memo** for components in lists
4. **useShallow** for Zustand object selectors
5. **Suspense boundary** at layout level, not per-route

---

## Anti-patterns - NEVER

| Don't | Why | Instead |
|-------|-----|---------|
| Inline functions in JSX for memo children | New reference = re-render | `useCallback` |
| Zustand selector without `useShallow` | Infinite render loop | Wrap in `useShallow` |
| `any` in TypeScript | No type safety | `unknown` + type guard |
| Index as key in lists | Breaks reconciliation | Stable unique ID |
| State in URL + useState | Duplication | URL only (useSearchParams) |
