---
name: zod-validation
description: Zod schema validation patterns for TypeScript applications. Use when the project is configured with Zod for runtime validation and type inference.
---

# Zod Validation Patterns

## Purpose

Schema validation and type inference using Zod for type-safe runtime validation.

## When to Use This Skill

- Validating API responses
- Form validation
- Environment variable validation
- Type inference from schemas

---

## Quick Reference

### Basic Schema

```typescript
import { z } from 'zod';

// Define schema
const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  age: z.number().int().positive().optional(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;

// Validate data
const result = userSchema.safeParse(data);
if (result.success) {
  const user: User = result.data;
} else {
  console.error(result.error.issues);
}
```

---

## Schema Definitions

### Primitive Types

```typescript
// Strings
z.string()
z.string().min(1)              // Required (non-empty)
z.string().max(100)            // Max length
z.string().email()             // Email format
z.string().url()               // URL format
z.string().uuid()              // UUID format
z.string().regex(/pattern/)    // Custom regex

// Numbers
z.number()
z.number().int()               // Integer
z.number().positive()          // > 0
z.number().nonnegative()       // >= 0
z.number().min(0).max(100)     // Range

// Others
z.boolean()
z.date()
z.null()
z.undefined()
z.literal('active')            // Exact value
```

### Objects

```typescript
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
  metadata: z.record(z.string()), // Record<string, string>
});

// Partial (all optional)
const partialUserSchema = userSchema.partial();

// Pick specific fields
const userCredentialsSchema = userSchema.pick({
  email: true,
  password: true,
});

// Omit fields
const createUserSchema = userSchema.omit({ id: true });

// Extend
const adminSchema = userSchema.extend({
  permissions: z.array(z.string()),
});
```

### Arrays

```typescript
z.array(z.string())                    // string[]
z.array(z.string()).nonempty()         // At least one item
z.array(z.string()).min(1).max(10)     // 1-10 items
z.string().array()                     // Alternative syntax
```

### Unions and Enums

```typescript
// Enum
const statusSchema = z.enum(['pending', 'active', 'inactive']);
type Status = z.infer<typeof statusSchema>; // 'pending' | 'active' | 'inactive'

// Union
const idSchema = z.union([z.string(), z.number()]);

// Discriminated union
const resultSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: z.any() }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);
```

---

## API Response Validation

```typescript
// schemas.ts
export const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

export const usersResponseSchema = z.object({
  data: z.array(userSchema),
  meta: z.object({
    page: z.number(),
    total: z.number(),
  }),
});

export type User = z.infer<typeof userSchema>;
export type UsersResponse = z.infer<typeof usersResponseSchema>;

// api.ts
export const fetchUsers = async (): Promise<UsersResponse> => {
  const response = await api.get('/users');
  return usersResponseSchema.parse(response.data);
};
```

---

## Form Validation

### With React Hook Form

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const formSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof formSchema>;

export const LoginForm = () => {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = (data: FormData) => {
    // data is validated and typed
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('email')} />
      {form.formState.errors.email && (
        <span>{form.formState.errors.email.message}</span>
      )}
      {/* ... */}
    </form>
  );
};
```

---

## Transformations

```typescript
// Transform during parsing
const schema = z.string().transform(val => val.toLowerCase());

// Coerce types
z.coerce.number()   // "123" -> 123
z.coerce.boolean()  // "true" -> true
z.coerce.date()     // "2024-01-01" -> Date

// Default values
const schema = z.object({
  name: z.string(),
  role: z.string().default('user'),
  active: z.boolean().default(true),
});

// Optional with default
z.string().optional().default('')
```

---

## Custom Validation

```typescript
// Custom validation with refine
const passwordSchema = z.string()
  .min(8)
  .refine(
    (val) => /[A-Z]/.test(val),
    { message: 'Must contain uppercase letter' }
  )
  .refine(
    (val) => /[0-9]/.test(val),
    { message: 'Must contain number' }
  );

// Custom error messages
const userSchema = z.object({
  email: z.string({
    required_error: 'Email is required',
    invalid_type_error: 'Email must be a string',
  }).email('Invalid email format'),
});

// Async validation
const uniqueEmailSchema = z.string().email().refine(
  async (email) => {
    const exists = await checkEmailExists(email);
    return !exists;
  },
  { message: 'Email already exists' }
);
```

---

## Error Handling

```typescript
// Safe parsing (doesn't throw)
const result = schema.safeParse(data);
if (!result.success) {
  const errors = result.error.flatten();
  // errors.fieldErrors - per-field errors
  // errors.formErrors - form-level errors
}

// Format errors for display
const formatZodErrors = (error: z.ZodError): Record<string, string> => {
  return Object.fromEntries(
    error.issues.map(issue => [
      issue.path.join('.'),
      issue.message,
    ])
  );
};
```

---

## Core Principles

1. **Schema First** - Define schemas before using data
2. **Type Inference** - Use `z.infer<>` for TypeScript types
3. **Validate at Boundaries** - API responses, form inputs
4. **Safe Parsing** - Use `safeParse` for user input
5. **Reusable Schemas** - Extract common patterns
