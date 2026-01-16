---
name: tanstack-query
description: TanStack Query (React Query) patterns for data fetching, caching, and mutations. Use when the project is configured with TanStack Query for server state management.
---

# TanStack Query Patterns

## Purpose

Data fetching and server state management patterns using TanStack Query (React Query).

## When to Use This Skill

- Fetching data from APIs
- Implementing mutations (create, update, delete)
- Managing cache and invalidation
- Setting up query options

---

## Quick Reference

### Query Options Factory Pattern

```typescript
// api/users/queries.ts
import { queryOptions } from '@tanstack/react-query';
import { fetchUser, fetchUsers } from './api';

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
```

---

## Data Fetching

### useSuspenseQuery (Recommended with Suspense)

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { userQueries } from '@/api/users/queries';

export const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {
  // No need for loading state - Suspense handles it
  const { data: user } = useSuspenseQuery(userQueries.detail(userId));

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
};

// Wrap in Suspense boundary
<Suspense fallback={<LoadingSpinner />}>
  <UserProfile userId={id} />
</Suspense>
```

### useQuery (Manual Loading State)

```typescript
import { useQuery } from '@tanstack/react-query';
import { userQueries } from '@/api/users/queries';

export const UserList: React.FC = () => {
  const { data, isLoading, error } = useQuery(userQueries.all());

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data?.length) return <EmptyState />;

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

---

## Mutations

### Basic Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createUser } from '@/api/users/api';

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Usage
const createUser = useCreateUser();

const handleSubmit = (data: CreateUserData) => {
  createUser.mutate(data, {
    onSuccess: () => {
      toast.success('User created!');
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });
};
```

### Optimistic Updates

```typescript
export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['users', newUser.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(['users', newUser.id]);

      // Optimistically update
      queryClient.setQueryData(['users', newUser.id], newUser);

      // Return context with snapshot
      return { previousUser };
    },
    onError: (err, newUser, context) => {
      // Rollback on error
      if (context?.previousUser) {
        queryClient.setQueryData(['users', newUser.id], context.previousUser);
      }
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
```

---

## Cache Management

### Invalidation Patterns

```typescript
const queryClient = useQueryClient();

// Invalidate all users queries
queryClient.invalidateQueries({ queryKey: ['users'] });

// Invalidate specific user
queryClient.invalidateQueries({ queryKey: ['users', userId] });

// Invalidate exact match only
queryClient.invalidateQueries({
  queryKey: ['users', 'list'],
  exact: true,
});

// Invalidate with predicate
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'users' &&
    query.state.data?.some(u => u.status === 'pending'),
});
```

### Prefetching

```typescript
// Prefetch on hover
const prefetchUser = (id: string) => {
  queryClient.prefetchQuery(userQueries.detail(id));
};

<li
  onMouseEnter={() => prefetchUser(user.id)}
  onClick={() => navigate(`/users/${user.id}`)}
>
  {user.name}
</li>
```

---

## Query Key Patterns

```typescript
// Hierarchical key structure
const queryKeys = {
  users: {
    all: ['users'] as const,
    lists: () => [...queryKeys.users.all, 'list'] as const,
    list: (filters: Filters) => [...queryKeys.users.lists(), filters] as const,
    details: () => [...queryKeys.users.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.users.details(), id] as const,
  },
};

// Usage
queryClient.invalidateQueries({ queryKey: queryKeys.users.all });
queryClient.invalidateQueries({ queryKey: queryKeys.users.detail(userId) });
```

---

## Error Handling

```typescript
// Global error handler in QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
    mutations: {
      onError: (error) => {
        toast.error(error.message);
      },
    },
  },
});

// Query-specific error handling
const { data, error } = useQuery({
  ...userQueries.detail(id),
  throwOnError: false, // Don't throw to error boundary
});

if (error) {
  return <ErrorComponent error={error} />;
}
```

---

## Dependent Queries

```typescript
// Query that depends on another
const { data: user } = useQuery(userQueries.detail(userId));

const { data: posts } = useQuery({
  queryKey: ['posts', user?.id],
  queryFn: () => fetchUserPosts(user!.id),
  enabled: !!user, // Only run when user exists
});
```

---

## Core Principles

1. **Query Options Factory** - Centralize query configurations
2. **Suspense First** - Use useSuspenseQuery when possible
3. **Proper Keys** - Hierarchical, consistent query keys
4. **Smart Invalidation** - Invalidate related queries after mutations
5. **Optimistic Updates** - For better UX on mutations
