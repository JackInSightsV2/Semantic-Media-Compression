'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import situationalAwareness from '@/demo-data/situational_awareness.json';

// JSON syntax highlighter component
function JsonHighlight({ data, indent = 0 }: { data: any; indent?: number }) {
  const indentStr = '  '.repeat(indent);

  if (data === null) {
    return <span className="text-purple-400">null</span>;
  }

  if (typeof data === 'boolean') {
    return <span className="text-purple-400">{data.toString()}</span>;
  }

  if (typeof data === 'number') {
    return <span className="text-blue-400">{data}</span>;
  }

  if (typeof data === 'string') {
    return <span className="text-green-400">&quot;{data}&quot;</span>;
  }

  if (Array.isArray(data)) {
    if (data.length === 0) {
      return <span className="text-gray-300">[]</span>;
    }
    return (
      <>
        <span className="text-gray-300">[</span>
        {'\n'}
        {data.map((item, i) => (
          <span key={i}>
            {indentStr}  <JsonHighlight data={item} indent={indent + 1} />
            {i < data.length - 1 ? <span className="text-gray-300">,</span> : ''}
            {'\n'}
          </span>
        ))}
        {indentStr}<span className="text-gray-300">]</span>
      </>
    );
  }

  if (typeof data === 'object') {
    const keys = Object.keys(data);
    if (keys.length === 0) {
      return <span className="text-gray-300">{'{}'}</span>;
    }
    return (
      <>
        <span className="text-gray-300">{'{'}</span>
        {'\n'}
        {keys.map((key, i) => (
          <span key={key}>
            {indentStr}  <span className="text-cyan-400">&quot;{key}&quot;</span>
            <span className="text-gray-300">: </span>
            <JsonHighlight data={data[key]} indent={indent + 1} />
            {i < keys.length - 1 ? <span className="text-gray-300">,</span> : ''}
            {'\n'}
          </span>
        ))}
        {indentStr}<span className="text-gray-300">{'}'}</span>
      </>
    );
  }

  return <span>{String(data)}</span>;
}

export default function ViewJsonPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const handleClickOutside = () => setIsMenuOpen(false);
    if (isMenuOpen) {
      document.addEventListener('click', handleClickOutside);
    }
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isMenuOpen]);

  useEffect(() => {
    if (isSidebarOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isSidebarOpen]);

  return (
    <div className="h-screen bg-gray-50 overflow-hidden flex flex-col">
      <header className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-[60]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8 flex-1">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h1 className="text-xl md:text-2xl font-bold text-gray-900">SemanticGuard</h1>
            </div>
            
            <div className="flex items-center gap-6">
              <div className="relative">
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    setIsMenuOpen(!isMenuOpen);
                  }}
                  className="lg:hidden text-gray-700 font-medium text-sm flex items-center gap-1 hover:text-gray-900"
                >
                  Menu
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {isMenuOpen && (
                  <div className="absolute top-full left-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg py-2 min-w-[160px] z-50">
                    <Link href="/" className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      Dashboard
                    </Link>
                    <button className="w-full text-left px-4 py-2 text-sm text-blue-600 font-medium hover:bg-gray-50">
                      Register Content
                    </button>
                    <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      Compare
                    </button>
                  </div>
                )}
              </div>
              
              <nav className="hidden lg:flex items-center gap-6">
                <Link href="/" className="text-gray-600 hover:text-gray-900 text-sm">
                  Dashboard
                </Link>
                <button className="text-blue-600 font-medium border-b-2 border-blue-600 pb-1 text-sm">
                  Register Content
                </button>
                <Link href="/compare" className="text-gray-600 hover:text-gray-900 text-sm">
                  Compare
                </Link>
              </nav>
              
              <div className="hidden xl:block relative w-80">
                <input 
                  type="text" 
                  placeholder="Search content, disputes, or analytics..." 
                  className="w-full bg-gray-100 rounded-full px-4 py-2 pl-10 text-sm outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white"
                />
                <svg className="absolute left-3 top-2.5 w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2 md:gap-4">
            <button className="relative p-2 text-gray-600 hover:text-gray-800 transition-colors" style={{marginTop: '3px'}}>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <div className="absolute top-1 right-1 w-4 h-4 bg-red-600 rounded-full flex items-center justify-center">
                <span className="text-white text-xs font-semibold">3</span>
              </div>
            </button>
            
            <button className="w-5 h-5 bg-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors">
              <span className="text-white font-semibold text-xs">?</span>
            </button>
            
            <button className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <img 
                src="/profile.jpg" 
                alt="Stephen Henry" 
                className="w-9 h-9 rounded-full object-cover"
              />
              <span className="hidden md:block text-sm font-medium text-gray-700">Stephen Henry</span>
              <svg className="hidden md:block w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
        </div>
      </header>
      
      {/* Mobile sidebar backdrop */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside 
          className={`
            fixed lg:static inset-y-0 left-0 
            w-64 bg-white border-r border-gray-200 
            transform transition-transform duration-300 ease-in-out
            z-50 lg:z-auto
            ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          `}
        >
          <div className="h-full overflow-y-auto p-4">
            <button 
              onClick={() => setIsSidebarOpen(false)}
              className="lg:hidden absolute top-4 right-4 text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <div className="mb-6">
              <h2 className="text-xs font-bold text-gray-700">MAIN MENU</h2>
              
              <div className="mt-3 space-y-1">
                <Link 
                  href="/"
                  className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <span className="text-sm">Dashboard</span>
                </Link>
                
                <Link 
                  href="/register"
                  className="w-full flex items-center gap-3 px-3 py-2 text-blue-600 bg-blue-50 rounded-lg font-medium"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  <span className="text-sm">Register Content</span>
                </Link>
                
                <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <span className="text-sm">My Library</span>
                </button>
              </div>
            </div>
          </div>
        </aside>

        <main className="flex-1 p-4 md:p-8 overflow-y-auto relative">
          <div className="fixed inset-0 bg-cover bg-center bg-no-repeat opacity-5 pointer-events-none" style={{ backgroundImage: 'url(/graph1.jpg)', left: 'auto', right: 0, width: 'calc(100% - 256px)' }}></div>
          <div className="relative z-10">
            <Link href="/register" className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span>Back to Register</span>
            </Link>

            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Semantic Fingerprint JSON</h1>
              <p className="text-gray-600 text-sm">
                View the complete semantic fingerprint data structure
              </p>
            </div>

            {/* JSON Content Viewer */}
            <div className="bg-gray-900 rounded-lg border border-gray-700 overflow-hidden">
              <div className="bg-gray-800 px-4 py-2 border-b border-gray-700 flex items-center justify-between">
                <span className="text-gray-300 text-sm font-medium">situational_awareness.json</span>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(JSON.stringify(situationalAwareness, null, 2));
                  }}
                  className="text-gray-400 hover:text-gray-200 text-sm flex items-center gap-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Copy
                </button>
              </div>
              <div className="overflow-auto max-h-[calc(100vh-280px)] p-6">
                <pre className="text-sm">
                  <code className="language-json">
                    <JsonHighlight data={situationalAwareness} />
                  </code>
                </pre>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

