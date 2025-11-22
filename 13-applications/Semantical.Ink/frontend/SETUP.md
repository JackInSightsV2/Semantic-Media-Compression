# Frontend Setup Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   ```
   Then edit `.env.local` with your Supabase credentials and API URL.

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## What's Included

### ✅ Framework & Tools
- Next.js 15 with App Router
- React 19
- TypeScript
- Tailwind CSS 4
- ESLint

### ✅ UI Components (shadcn/ui)
- Button (with variants)
- Card
- Input

### ✅ Utilities
- Supabase client setup
- API client setup
- Utility functions (cn for className merging)

### ✅ Project Structure
- App Router structure ready
- Component directories organized
- TypeScript configuration
- Tailwind configuration with shadcn/ui theme

## Adding More shadcn/ui Components

To add additional components from shadcn/ui:

```bash
npx shadcn@latest add [component-name]
```

Popular components to add:
- `dialog` - Modal dialogs
- `dropdown-menu` - Dropdown menus
- `select` - Select inputs
- `textarea` - Text areas
- `label` - Form labels
- `tabs` - Tab navigation
- `avatar` - User avatars
- `badge` - Badges/tags
- `skeleton` - Loading skeletons
- `toast` - Toast notifications

Example:
```bash
npx shadcn@latest add dialog dropdown-menu select
```

## Next Steps

1. **Add more UI components** as needed
2. **Set up Supabase authentication** in `lib/supabase.ts`
3. **Create landing page components** in `components/landing/`
4. **Build Produce page** in `app/produce/`
5. **Integrate backend API** using `lib/api.ts`

## Troubleshooting

### Port already in use
If port 3000 is taken, Next.js will automatically use the next available port.

### TypeScript errors
Make sure all dependencies are installed:
```bash
npm install
```

### Tailwind not working
Check that `postcss.config.mjs` exists and `tailwind.config.ts` is configured correctly.

### shadcn/ui components not found
Make sure `components.json` exists and paths are correct in `tsconfig.json`.

