'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface RegisteredContentContextType {
  registeredContentIds: string[];
  isContentRegistered: (contentId: string) => boolean;
  registerContent: (contentId: string) => void;
  clearAllRegistrations: () => void;
}

const RegisteredContentContext = createContext<RegisteredContentContextType | undefined>(undefined);

export function RegisteredContentProvider({ children }: { children: ReactNode }) {
  const [registeredContentIds, setRegisteredContentIds] = useState<string[]>([]);
  
  // No persistence - resets on page reload for demo purposes

  const isContentRegistered = (contentId: string): boolean => {
    return registeredContentIds.includes(contentId);
  };

  const registerContent = (contentId: string) => {
    setRegisteredContentIds(prev => {
      if (!prev.includes(contentId)) {
        return [...prev, contentId];
      }
      return prev;
    });
  };

  const clearAllRegistrations = () => {
    setRegisteredContentIds([]);
  };

  return (
    <RegisteredContentContext.Provider
      value={{
        registeredContentIds,
        isContentRegistered,
        registerContent,
        clearAllRegistrations,
      }}
    >
      {children}
    </RegisteredContentContext.Provider>
  );
}

export function useRegisteredContent() {
  const context = useContext(RegisteredContentContext);
  if (context === undefined) {
    throw new Error('useRegisteredContent must be used within a RegisteredContentProvider');
  }
  return context;
}

