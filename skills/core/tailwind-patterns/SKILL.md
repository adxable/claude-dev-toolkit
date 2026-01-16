---
name: tailwind-patterns
description: Tailwind CSS patterns and conventions for consistent styling in React applications. Covers utility classes, responsive design, and component styling.
---

# Tailwind CSS Patterns

## Purpose

Styling guide using Tailwind CSS utility classes for consistent, maintainable React components.

## When to Use This Skill

- Styling components
- Responsive design
- Layout patterns
- Custom theming

---

## Quick Reference

### Spacing Scale

| Class | Value |
|-------|-------|
| `p-1` / `m-1` | 0.25rem (4px) |
| `p-2` / `m-2` | 0.5rem (8px) |
| `p-4` / `m-4` | 1rem (16px) |
| `p-6` / `m-6` | 1.5rem (24px) |
| `p-8` / `m-8` | 2rem (32px) |

### Common Patterns

```tsx
// Card
<div className="rounded-lg border bg-card p-6 shadow-sm">

// Flex row with gap
<div className="flex items-center gap-4">

// Flex column
<div className="flex flex-col gap-2">

// Grid
<div className="grid grid-cols-3 gap-4">

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

---

## Layout Patterns

### Centering

```tsx
// Horizontal center
<div className="flex justify-center">

// Vertical center
<div className="flex items-center">

// Both (center everything)
<div className="flex items-center justify-center">

// Full page center
<div className="flex min-h-screen items-center justify-center">
```

### Page Layout

```tsx
// Standard page with sidebar
<div className="flex h-screen">
  <aside className="w-64 border-r bg-muted">
    {/* Sidebar */}
  </aside>
  <main className="flex-1 overflow-auto p-6">
    {/* Content */}
  </main>
</div>

// Page with header
<div className="flex min-h-screen flex-col">
  <header className="sticky top-0 z-50 border-b bg-background">
    {/* Header */}
  </header>
  <main className="flex-1 p-6">
    {/* Content */}
  </main>
</div>
```

### Container

```tsx
// Centered container with max width
<div className="container mx-auto px-4">

// Constrained width
<div className="mx-auto max-w-4xl px-4">
```

---

## Component Patterns

### Buttons

```tsx
// Primary button
<button className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">
  Primary
</button>

// Secondary button
<button className="rounded-md border bg-background px-4 py-2 text-sm font-medium hover:bg-accent">
  Secondary
</button>

// Danger button
<button className="rounded-md bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground hover:bg-destructive/90">
  Delete
</button>

// Icon button
<button className="rounded-md p-2 hover:bg-accent">
  <Icon className="h-4 w-4" />
</button>
```

### Cards

```tsx
// Basic card
<div className="rounded-lg border bg-card p-6">
  <h3 className="text-lg font-semibold">{title}</h3>
  <p className="mt-2 text-muted-foreground">{description}</p>
</div>

// Clickable card
<div className="cursor-pointer rounded-lg border bg-card p-6 transition-colors hover:bg-accent">
  {/* Content */}
</div>

// Card with header and footer
<div className="rounded-lg border bg-card">
  <div className="border-b p-4">
    <h3 className="font-semibold">{title}</h3>
  </div>
  <div className="p-4">
    {/* Content */}
  </div>
  <div className="border-t bg-muted/50 p-4">
    {/* Footer */}
  </div>
</div>
```

### Forms

```tsx
// Form field
<div className="space-y-2">
  <label className="text-sm font-medium">{label}</label>
  <input
    className="w-full rounded-md border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
    type="text"
  />
  <p className="text-sm text-muted-foreground">{hint}</p>
</div>

// Form with sections
<form className="space-y-6">
  <div className="space-y-4">
    {/* Field group */}
  </div>
  <div className="flex justify-end gap-2">
    <button type="button">Cancel</button>
    <button type="submit">Submit</button>
  </div>
</form>
```

### Lists

```tsx
// Simple list
<ul className="space-y-2">
  {items.map(item => (
    <li key={item.id} className="rounded-md border p-3">
      {item.name}
    </li>
  ))}
</ul>

// Interactive list
<ul className="divide-y">
  {items.map(item => (
    <li
      key={item.id}
      className="flex cursor-pointer items-center gap-3 p-3 hover:bg-accent"
    >
      {item.name}
    </li>
  ))}
</ul>
```

---

## Responsive Design

### Breakpoints

| Prefix | Min Width |
|--------|-----------|
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

### Mobile-First Pattern

```tsx
// Stack on mobile, row on desktop
<div className="flex flex-col gap-4 md:flex-row">

// Full width on mobile, auto on desktop
<div className="w-full md:w-auto">

// Hide on mobile, show on desktop
<div className="hidden md:block">

// Show on mobile, hide on desktop
<div className="block md:hidden">

// Responsive grid
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
```

---

## Text Styling

```tsx
// Headings
<h1 className="text-4xl font-bold tracking-tight">Heading 1</h1>
<h2 className="text-3xl font-semibold">Heading 2</h2>
<h3 className="text-2xl font-semibold">Heading 3</h3>

// Body text
<p className="text-base text-foreground">Regular text</p>
<p className="text-sm text-muted-foreground">Secondary text</p>
<p className="text-xs text-muted-foreground">Small text</p>

// Truncate long text
<p className="truncate">Very long text that will be truncated</p>
<p className="line-clamp-2">Text limited to 2 lines</p>
```

---

## Color System

### Semantic Colors

```tsx
// Background
bg-background     // Main background
bg-card           // Card background
bg-muted          // Muted background
bg-accent         // Accent/hover background

// Text
text-foreground         // Primary text
text-muted-foreground   // Secondary text
text-primary            // Brand color text

// Borders
border            // Default border
border-muted      // Muted border

// Status colors
bg-destructive text-destructive-foreground  // Error/danger
text-green-600    // Success
text-yellow-600   // Warning
```

---

## Conditional Classes

### Using clsx or cn

```tsx
import { cn } from '@/lib/utils';

// Conditional classes
<div
  className={cn(
    'rounded-md p-4',
    isActive && 'bg-primary text-primary-foreground',
    disabled && 'opacity-50 pointer-events-none'
  )}
>

// Variant-based styling
<button
  className={cn(
    'rounded-md px-4 py-2 font-medium',
    {
      'bg-primary text-primary-foreground': variant === 'primary',
      'border bg-background': variant === 'secondary',
      'bg-destructive text-destructive-foreground': variant === 'danger',
    }
  )}
>
```

---

## Core Principles

1. **Utility-First** - Use utility classes, not custom CSS
2. **Mobile-First** - Start with mobile, add breakpoints
3. **Semantic Colors** - Use theme colors (bg-card, text-muted-foreground)
4. **Consistent Spacing** - Use the spacing scale (p-4, gap-2, etc.)
5. **Composition** - Combine utilities for complex designs
