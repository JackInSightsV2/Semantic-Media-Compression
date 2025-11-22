# Semantical.Ink Frontend

Next.js 15 frontend application with shadcn/ui components and Tailwind CSS.

## Tech Stack

- **Next.js 15** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - UI component library
- **Supabase** - Authentication and database

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your configuration:
   - Supabase URL and anon key
   - Backend API URL

4. Run development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   ├── globals.css         # Global styles
│   ├── produce/           # Produce page (main product)
│   ├── marketplace/       # Marketplace/gallery
│   ├── library/           # Content library
│   ├── dashboard/         # Creator dashboard
│   └── protection/        # Protection features
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── landing/           # Landing page components
│   ├── produce/           # Produce page components
│   ├── marketplace/       # Marketplace components
│   ├── protection/        # Protection components
│   └── dashboard/         # Dashboard components
├── lib/
│   ├── utils.ts           # Utility functions
│   ├── supabase.ts        # Supabase client
│   └── api.ts             # Backend API client
└── public/                 # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Adding shadcn/ui Components

To add more shadcn/ui components:

```bash
npx shadcn@latest add [component-name]
```

For example:
```bash
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
```

## Environment Variables

See `.env.example` for required environment variables.

## Development

The app uses:
- **App Router** - Next.js 15 App Router for routing
- **Server Components** - Default, use Client Components when needed (`'use client'`)
- **TypeScript** - Full type safety
- **Tailwind CSS** - Utility-first CSS framework

## Next Steps

1. Set up Supabase authentication
2. Create landing page components
3. Build Produce page interface
4. Integrate backend API
5. Add marketplace features

