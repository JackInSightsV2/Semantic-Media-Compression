'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function RegisterPage() {
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
                    <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      My Content
                    </button>
                    <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      Disputes
                    </button>
                    <button className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      Analytics
                    </button>
                  </div>
                )}
              </div>

              <nav className="hidden lg:flex items-center gap-6">
                <Link href="/" className="text-gray-600 hover:text-gray-900 text-sm">
                  Dashboard
                </Link>
                <button className="text-gray-600 hover:text-gray-900 text-sm">
                  My Content
                </button>
                <button className="text-gray-600 hover:text-gray-900 text-sm">
                  Disputes
                </button>
                <button className="text-gray-600 hover:text-gray-900 text-sm">
                  Analytics
                </button>
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
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <div className="flex flex-1 overflow-hidden relative">
        <div className="fixed left-4 bottom-[36px] z-40">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <aside className={`
          fixed lg:static top-0 left-0 h-screen lg:h-full
          w-64 bg-white border-r border-gray-200 p-4 z-50
          transform transition-transform duration-300 ease-in-out
          overflow-y-auto
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}>
          <div className="lg:hidden flex justify-end mb-4">
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="p-2 text-gray-600 hover:text-gray-900"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Quick Actions */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">QUICK ACTIONS</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="text-sm font-medium">New Report</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span className="text-sm">Import Data</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
                <span className="text-sm">Share Dashboard</span>
              </button>
            </div>
          </div>

          {/* Navigation */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">NAVIGATION</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-sm">Overview</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-sm">Analytics</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-blue-600 bg-blue-50 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm font-medium">Reports</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span className="text-sm">Settings</span>
              </button>
            </div>
          </div>

          {/* Recent Projects */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">RECENT PROJECTS</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg text-left">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                  </svg>
                </div>
                <div className="flex-1 min-w-0 text-left">
                  <div className="font-medium text-gray-900 text-sm">Q4 Sales Analysis</div>
                  <div className="text-xs text-gray-500">Updated 2h ago</div>
                </div>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg text-left">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div className="flex-1 min-w-0 text-left">
                  <div className="font-medium text-gray-900 text-sm">User Engagement</div>
                  <div className="text-xs text-gray-500">Updated 5h ago</div>
                </div>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg text-left">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div className="flex-1 min-w-0 text-left">
                  <div className="font-medium text-gray-900 text-sm">Product Launch</div>
                  <div className="text-xs text-gray-500">Updated 1d ago</div>
                </div>
              </button>
            </div>
          </div>

          <div className="absolute bottom-[36px] right-4">
            <button className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          </div>
        </aside>

        <main className="flex-1 p-4 md:p-8 overflow-y-auto">
          <Link href="/" className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>Back</span>
          </Link>

          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Register Semantic IP</h1>
            <p className="text-gray-600 text-sm">
              Protect your creative content with blockchain-based intellectual property registration
            </p>
          </div>

          {/* Select Content Section */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-lg">1</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Select Content</h2>
            </div>

            {/* Content Card with Gradient */}
            <div className="bg-gradient-to-r from-blue-50 to-pink-50 rounded-lg border border-blue-100 p-6">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>

                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Demo Content 1: The Crossroads Decision</h3>
                    <p className="text-gray-600 mb-4">Selected content ready for semantic fingerprint generation</p>

                    <div className="flex items-center gap-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-600 text-white">
                        Selected
                      </span>
                      <span className="text-gray-600 text-sm">Content Type: Narrative</span>
                      <span className="text-gray-600 text-sm">Genre: Psychological Thriller</span>
                    </div>
                  </div>
                </div>

                <button className="text-blue-600 hover:text-blue-700 p-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {/* Preview Semantic Fingerprint Section */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-lg">2</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Preview Semantic Fingerprint</h2>
            </div>

            {/* Content Preview Card */}
            <div className="bg-gray-100 rounded-lg p-6 mb-6">
              <div className="flex items-start gap-4">
                <div className="text-4xl">🎬</div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-1">The Crossroads Decision</h3>
                  <p className="text-gray-600">A visual exploration of moral choices and their consequences</p>
                </div>
              </div>
            </div>

            {/* Grid of 4 Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Narrative Structure */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <h4 className="font-bold text-gray-900">Narrative Structure</h4>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Genre</span>
                    <span className="text-gray-600 text-right">psychological thriller</span>
                  </div>
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Story Arc</span>
                    <span className="text-gray-600 text-right">individual confronting moral crisis</span>
                  </div>
                  <div>
                    <div className="text-gray-700 font-medium mb-2">Themes</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">choice and consequence</span>
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">identity under pressure</span>
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">isolation</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Progression</span>
                    <span className="text-gray-600 text-right">contemplation → crisis → resolution</span>
                  </div>
                </div>
              </div>

              {/* Character Essence */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <h4 className="font-bold text-gray-900">Character Essence</h4>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Archetype</span>
                    <span className="text-gray-600 text-right">reluctant hero</span>
                  </div>
                  <div>
                    <div className="text-gray-700 font-medium mb-2">Traits</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">analytical</span>
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">conflicted</span>
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">determined</span>
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">introspective</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Character Arc</span>
                    <span className="text-gray-600 text-right">isolated → forced to engage → transformed</span>
                  </div>
                </div>
              </div>

              {/* Thematic Content */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                  </svg>
                  <h4 className="font-bold text-gray-900">Thematic Content</h4>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Primary Theme</span>
                    <span className="text-gray-600 text-right">consequences of choice</span>
                  </div>
                  <div>
                    <div className="text-gray-700 font-medium mb-2">Secondary Themes</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">isolation vs connection</span>
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">duty vs desire</span>
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">truth vs comfort</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-start">
                    <span className="text-gray-700 font-medium">Emotional Tone</span>
                    <span className="text-gray-600 text-right">tense contemplation building to resolve</span>
                  </div>
                  <div>
                    <div className="text-gray-700 font-medium mb-2">Visual Metaphors</div>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">crossroads</span>
                      <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">heights suggesting risk</span>
                      <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">shadows representing doubt</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Fingerprint Summary */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <h4 className="font-bold text-gray-900">Fingerprint Summary</h4>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="text-gray-700 font-medium mb-2">Semantic Hash</div>
                    <div className="bg-gray-50 rounded p-3 font-mono text-xs break-all text-gray-700">
                      0x4a7b8c9d2e3f4g5h6i7j8k910m1n2o3p4q5r6s7t8u9v0w1x2y3z
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 rounded-lg p-4 text-center">
                      <div className="text-3xl font-bold text-blue-600 mb-1">94%</div>
                      <div className="text-sm text-gray-600">Uniqueness Score</div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 text-center">
                      <div className="text-3xl font-bold text-green-600 mb-1">High</div>
                      <div className="text-sm text-gray-600">Protection Level</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Approve Button */}
            <div className="flex justify-end">
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                Approve Fingerprint
              </button>
            </div>
          </div>

          {/* Register on Blockchain Section */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gray-400 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-lg">3</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Register on Blockchain</h2>
            </div>

            {/* Content Area */}
            <div className="bg-gray-50 rounded-lg p-12 text-center">
              {/* Shield Icon */}
              <div className="flex justify-center mb-6">
                <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
              </div>

              <h3 className="text-2xl font-bold text-gray-700 mb-2">Register IP Asset on Story Protocol</h3>
              <p className="text-gray-600 mb-8">Complete the fingerprint approval to proceed with blockchain registration</p>

              {/* Benefits Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="bg-white rounded-lg border border-gray-200 p-6">
                  <div className="flex justify-center mb-3">
                    <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-700 mb-1">Immutable Protection</h4>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                  <div className="flex justify-center mb-3">
                    <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-700 mb-1">Global Recognition</h4>
                </div>

                <div className="bg-white rounded-lg border border-gray-200 p-6">
                  <div className="flex justify-center mb-3">
                    <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-700 mb-1">Proof of Ownership</h4>
                </div>
              </div>

              {/* Register Button */}
              <div className="flex flex-col items-center">
                <button disabled className="bg-gray-300 text-gray-500 px-8 py-3 rounded-lg font-medium cursor-not-allowed flex items-center gap-2 mb-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  Register IP Asset
                </button>
                <p className="text-sm text-gray-500">Complete previous steps to enable registration</p>
              </div>
            </div>
          </div>

          {/* Registration Progress */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Registration Progress</h2>

            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-900 font-medium">Step 2 of 3 Complete</span>
              <div className="flex items-center gap-6">
                <span className="text-gray-900 font-bold">67%</span>
                <div className="text-right">
                  <div className="font-bold text-gray-900">Estimated Time</div>
                  <div className="text-sm text-gray-600">2-3 minutes remaining</div>
                </div>
              </div>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{width: '67%'}}></div>
            </div>
          </div>

          {/* Action Buttons - Outside of cards */}
          <div className="flex items-center justify-between mb-6">
            <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors">
              Save as Draft
            </button>

            <div className="flex items-center gap-3">
              <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                Previous Step
              </button>
              <button className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                Continue to Registration
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
