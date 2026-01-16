---
name: typescript-standards
description: TypeScript conventions and best practices for React applications. Covers type definitions, interfaces, generics, and type-safe patterns.
---

# TypeScript Standards

## Purpose

TypeScript conventions for React frontend development, ensuring type safety and maintainability.

## When to Use This Skill

- Defining types and interfaces
- Working with generics
- Fixing type errors
- Designing type-safe APIs

---

## Quick Reference

### Prefer Interface for Objects

```typescript
// ✅ Use interface for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

// ✅ Use type for unions, intersections, mapped types
type Status = 'pending' | 'active' | 'inactive';
type UserWithRole = User & { role: string };
```

### Type Imports

```typescript
// ✅ Use type imports for types only
import type { User, Post } from '@/types';
import { fetchUser } from '@/api';

// ✅ Inline type imports
import { type User, fetchUser } from '@/api';
```

---

## Component Props

### Basic Props

```typescript
interface ButtonProps {
  /** Button text label */
  label: string;
  /** Click handler */
  onClick: () => void;
  /** Whether button is disabled */
  disabled?: boolean;
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger';
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = 'primary'
}) => {
  // ...
};
```

### Props with Children

```typescript
interface CardProps {
  title: string;
  children: React.ReactNode;
}

interface CardWithRenderProps {
  data: User;
  renderHeader?: (user: User) => React.ReactNode;
}
```

### Extending HTML Props

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  ...inputProps
}) => {
  return (
    <div>
      <label>{label}</label>
      <input {...inputProps} />
      {error && <span className="text-red-500">{error}</span>}
    </div>
  );
};
```

---

## Generics

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor
}: ListProps<T>): React.ReactElement {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={user => <span>{user.name}</span>}
  keyExtractor={user => user.id}
/>
```

### Generic Hooks

```typescript
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [stored, setStored] = useState<T>(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setValue = useCallback((value: T) => {
    setStored(value);
    localStorage.setItem(key, JSON.stringify(value));
  }, [key]);

  return [stored, setValue];
}
```

---

## Utility Types

### Common Utilities

```typescript
// Partial - All properties optional
type PartialUser = Partial<User>;

// Required - All properties required
type RequiredUser = Required<User>;

// Pick - Select specific properties
type UserSummary = Pick<User, 'id' | 'name'>;

// Omit - Exclude specific properties
type UserWithoutId = Omit<User, 'id'>;

// Record - Key-value mapping
type UserById = Record<string, User>;

// Extract - Extract from union
type ActiveStatus = Extract<Status, 'active' | 'pending'>;

// Exclude - Remove from union
type InactiveStatus = Exclude<Status, 'active'>;
```

### Custom Utility Types

```typescript
// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// Deep partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

---

## Type Guards

```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

// Discriminated unions
interface SuccessResult {
  status: 'success';
  data: User;
}

interface ErrorResult {
  status: 'error';
  error: string;
}

type Result = SuccessResult | ErrorResult;

function handleResult(result: Result) {
  if (result.status === 'success') {
    // TypeScript knows result.data exists
    console.log(result.data.name);
  } else {
    // TypeScript knows result.error exists
    console.log(result.error);
  }
}
```

---

## Event Handlers

```typescript
// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

// Input events
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// Click events
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  // ...
};

// Keyboard events
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') {
    // ...
  }
};
```

---

## API Types

```typescript
// Request/Response types
interface ApiResponse<T> {
  data: T;
  meta: {
    page: number;
    total: number;
  };
}

interface ApiError {
  message: string;
  code: string;
  details?: Record<string, string>;
}

// Function types
type FetchUser = (id: string) => Promise<User>;
type UpdateUser = (id: string, data: Partial<User>) => Promise<User>;
```

---

## Strict Mode Rules

### No `any`

```typescript
// ❌ Avoid any
const data: any = fetchData();

// ✅ Use unknown + type guard
const data: unknown = fetchData();
if (isUser(data)) {
  console.log(data.name);
}

// ✅ Or use proper types
const data: User = await fetchUser(id);
```

### No Implicit Any

```typescript
// ❌ Implicit any in parameters
function process(data) { ... }

// ✅ Explicit types
function process(data: ProcessData): ProcessResult { ... }
```

### Non-null Assertions

```typescript
// ❌ Avoid non-null assertion when possible
const element = document.getElementById('root')!;

// ✅ Use type guard or conditional
const element = document.getElementById('root');
if (element) {
  // element is HTMLElement
}
```

---

## Core Principles

1. **Explicit Types** - Always type function parameters and returns
2. **Interface for Objects** - Use interface for object shapes
3. **No `any`** - Use unknown + type guards instead
4. **Type Imports** - Use `import type` for type-only imports
5. **Narrow Types** - Use discriminated unions and type guards
6. **Generic When Needed** - Use generics for reusable typed code
