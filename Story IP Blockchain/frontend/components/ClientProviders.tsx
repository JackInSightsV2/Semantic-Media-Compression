'use client';

import { RegisteredContentProvider } from '@/context/RegisteredContentContext';

export function ClientProviders({ children }: { children: React.ReactNode }) {
  return (
    <RegisteredContentProvider>
      {children}
    </RegisteredContentProvider>
  );
}

