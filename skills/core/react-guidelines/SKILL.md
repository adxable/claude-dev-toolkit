---
name: react-guidelines
description: React development guidelines covering component patterns, hooks, state management, and best practices. Core skill for all React frontend development.
---

# React Development Guidelines

## Purpose

Core architecture guide for React development, covering component patterns, hooks, state management, and best practices.

## When to Use This Skill

- Creating new components
- Implementing hooks
- Managing state
- Organizing React code

---

## Quick Start

### New Component Checklist

- [ ] Use functional components with TypeScript
- [ ] Define props interface
- [ ] Use hooks at the top level
- [ ] Memoize expensive computations
- [ ] Handle loading, error, empty states
- [ ] Use Suspense boundaries where appropriate
- [ ] Export as default at bottom

---

## Component Patterns

### Basic Component

```typescript
import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-4 py-2 rounded bg-primary text-white"
    >
      {label}
    </button>
  );
};

export default Button;
```

### Component with Hooks

```typescript
import React, { useState, useCallback, useMemo } from 'react';

interface ListProps {
  items: string[];
  onSelect: (item: string) => void;
}

export const List: React.FC<ListProps> = ({ items, onSelect }) => {
  const [filter, setFilter] = useState('');

  const filteredItems = useMemo(() =>
    items.filter(item => item.includes(filter)),
    [items, filter]
  );

  const handleSelect = useCallback((item: string) => {
    onSelect(item);
  }, [onSelect]);

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <ul>
        {filteredItems.map(item => (
          <li key={item} onClick={() => handleSelect(item)}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

### Lazy Loaded Component

```typescript
import React, { Suspense, lazy } from 'react';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const DataGrid = lazy(() => import('./DataGrid'));

export const Dashboard: React.FC = () => {
  return (
    <div>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>

      <Suspense fallback={<div>Loading data...</div>}>
        <DataGrid />
      </Suspense>
    </div>
  );
};
```

---

## Hooks Guidelines

### Rules of Hooks

1. Only call hooks at the top level
2. Only call hooks from React functions
3. Name custom hooks with `use` prefix

### Common Hooks

```typescript
// useState - Local state
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// useEffect - Side effects
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);

// useCallback - Memoized callbacks
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);

// useMemo - Memoized values
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// useRef - Mutable ref
const inputRef = useRef<HTMLInputElement>(null);
```

### Custom Hook Pattern

```typescript
import { useState, useCallback } from 'react';

interface UseToggleReturn {
  value: boolean;
  toggle: () => void;
  setTrue: () => void;
  setFalse: () => void;
}

export const useToggle = (initial = false): UseToggleReturn => {
  const [value, setValue] = useState(initial);

  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
};
```

---

## State Management

### Local vs Global State

| State Type | Solution | When to Use |
|------------|----------|-------------|
| Local UI | `useState` | Modal open, form inputs, local toggles |
| Shared UI | Context or Zustand | Theme, sidebar state, user preferences |
| Server data | TanStack Query / SWR | API data, remote state |
| URL state | URL params | Filters, pagination, search |

### State Colocation

Keep state as close to where it's used as possible:

```typescript
// ❌ Bad - State too high
const App = () => {
  const [modalOpen, setModalOpen] = useState(false);
  return <Dashboard modalOpen={modalOpen} setModalOpen={setModalOpen} />;
};

// ✅ Good - State colocated
const Dashboard = () => {
  const [modalOpen, setModalOpen] = useState(false);
  return <Modal open={modalOpen} onClose={() => setModalOpen(false)} />;
};
```

---

## Performance Guidelines

### When to Memoize

```typescript
// ✅ Memoize expensive computations
const sortedItems = useMemo(() =>
  items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// ✅ Memoize callbacks passed to children
const handleClick = useCallback(() => {
  doSomething();
}, []);

// ✅ Memoize components that receive objects/arrays as props
const MemoizedChild = React.memo(ChildComponent);

// ❌ Don't memoize simple values
const doubled = useMemo(() => count * 2, [count]); // Unnecessary
```

### React.memo Usage

```typescript
interface ItemProps {
  item: Item;
  onSelect: (id: string) => void;
}

// Memoize components that:
// 1. Render often
// 2. Receive the same props frequently
// 3. Have expensive render logic
export const ItemCard = React.memo<ItemProps>(({ item, onSelect }) => {
  return (
    <div onClick={() => onSelect(item.id)}>
      {item.name}
    </div>
  );
});
```

---

## Error Boundaries

```typescript
import React, { Component, ReactNode } from 'react';

interface ErrorBoundaryProps {
  fallback: ReactNode;
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Error caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<div>Something went wrong</div>}>
  <MyComponent />
</ErrorBoundary>
```

---

## File Organization

```
features/
  my-feature/
    components/
      MyFeature.tsx
      MyFeatureHeader.tsx
      MyFeatureContent.tsx
    hooks/
      useMyFeature.ts
    api/
      queries.ts
      mutations.ts
    types/
      index.ts
    index.ts  # Public exports
```

---

## Core Principles

1. **Composition over Inheritance** - Build complex UIs from simple components
2. **Single Responsibility** - Each component does one thing well
3. **Explicit over Implicit** - Clear props and types
4. **Colocate Related Code** - Keep state and logic near where it's used
5. **Optimize Last** - Don't prematurely optimize, measure first
