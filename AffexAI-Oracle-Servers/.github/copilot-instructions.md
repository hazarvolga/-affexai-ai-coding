# GitHub Copilot Instructions for New Frontend Integration

## Project Context
Integrating modern Next.js 15 + shadcn/ui frontend patterns into existing PayloadCMS website while preserving API contracts and admin functionality.

## Current Tech Stack
- **Next.js**: 15.4.4 with App Router
- **PayloadCMS**: 3.55.0 with PostgreSQL
- **UI Library**: Transitioning to shadcn/ui + Radix UI primitives
- **Styling**: Tailwind CSS with design tokens
- **Testing**: Jest + React Testing Library

## Recent Project Changes

### 2025-01-19: New Frontend Integration Planning
- Created comprehensive implementation plan for product catalog integration
- Established data model preserving PayloadCMS schema
- Defined API contracts for `/api/products` endpoints
- Set up development workflow with TDD approach

### Architecture Decisions
- **Component Strategy**: Import shadcn/ui patterns, preserve PayloadCMS Admin
- **Data Fetching**: Server Components for SEO, Client Components for interactivity
- **Styling**: Tailwind with CSS custom properties, scoped to avoid Admin conflicts
- **Performance**: Sub-200ms page loads via Server Components and code splitting

### Key Files and Patterns
- Product catalog: `/products` listing and `/products/[slug]` detail pages
- Component library: `src/components/ui/` for reusable primitives
- Type definitions: Focus on ProductCard and ProductDetail interfaces
- API integration: Preserve existing PayloadCMS REST endpoints

## Code Generation Guidelines

### TypeScript Interfaces
Always use these type definitions for product-related components:
```typescript
interface ProductCard {
  id: string;
  title: string;
  slug: string;
  price?: number;
  stock?: number;
  primaryImage?: {
    url: string;
    alt: string;
    width: number;
    height: number;
  };
  stockStatus: 'in-stock' | 'low-stock' | 'out-of-stock';
  priceFormatted?: string;
}
```

### Component Patterns
- Use Server Components by default for data fetching
- Add 'use client' directive only for interactive elements
- Import shadcn/ui components: `import { Button } from '@/components/ui/button'`
- Use Tailwind classes with CSS custom properties: `bg-background text-foreground`

### Data Fetching
```typescript
// Server Component pattern
async function ProductListing() {
  const response = await fetch('http://localhost:3000/api/products?where[status][equals]=published');
  const data = await response.json();
  return <ProductGrid products={data.docs} />;
}
```

### Accessibility Requirements
- Include skip links: `<a href="#main" className="sr-only focus:not-sr-only">Skip to main</a>`
- Use semantic HTML: `<main>`, `<nav>`, `<article>`, `<section>`
- ARIA labels for interactive elements
- Keyboard navigation support

## Development Priorities
1. **API Preservation**: Never modify existing `/api/*` endpoints
2. **Performance**: Maintain <200ms page loads
3. **Accessibility**: WCAG 2.2 AA compliance
4. **Testing**: TDD with contract tests for API integration
5. **Styling**: Consistent design system without breaking PayloadCMS Admin

## Files to Focus On
- `/src/app/(frontend)/products/page.tsx` - Product listing
- `/src/app/(frontend)/products/[slug]/page.tsx` - Product detail
- `/src/components/ui/` - Reusable UI primitives
- `/src/lib/utils.ts` - Utility functions and data transformers

## Testing Approach
- Contract tests for API compatibility
- Integration tests for user journeys
- Accessibility tests with axe-core
- Performance monitoring with Lighthouse CI
