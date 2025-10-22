'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';

export default function Dashboard() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [timeRange, setTimeRange] = useState('30');
  
  // Protection Activity Chart Data
  const activityData = [
    { date: 'Oct 1', contentRegistered: 2, matchesFound: 0, disputesFiled: 0 },
    { date: 'Oct 5', contentRegistered: 4, matchesFound: 1, disputesFiled: 0 },
    { date: 'Oct 10', contentRegistered: 3, matchesFound: 2, disputesFiled: 1 },
    { date: 'Oct 15', contentRegistered: 8, matchesFound: 3, disputesFiled: 1 },
    { date: 'Oct 20', contentRegistered: 6, matchesFound: 1, disputesFiled: 0 },
    { date: 'Oct 25', contentRegistered: 5, matchesFound: 2, disputesFiled: 1 },
    { date: 'Oct 30', contentRegistered: 8, matchesFound: 4, disputesFiled: 2 },
  ];
  
  // Semantic Match Distribution Data
  const matchDistributionData = [
    { name: 'High Match (≥85%)', value: 3, color: '#EF4444' },
    { name: 'Medium Match (50-85%)', value: 4, color: '#F59E0B' },
    { name: 'Low Match (<50%)', value: 8, color: '#3B82F6' },
  ];
  
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
                    <button className="w-full text-left px-4 py-2 text-sm text-blue-600 font-medium hover:bg-gray-50">
                      Dashboard
                    </button>
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
                <button className="text-blue-600 font-medium border-b-2 border-blue-600 pb-1 text-sm">
                  Dashboard
                </button>
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
          <button className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg">
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
          
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-white font-bold text-sm">Pro Plan</span>
              <span className="text-yellow-300 text-lg" style={{marginTop: '-4px'}}>👑</span>
            </div>
            <div className="text-white text-xs opacity-90 mb-3">
              2,847 / 5,000 content scans used
            </div>
            <div className="w-full rounded-full h-2" style={{backgroundColor: 'rgba(255, 255, 255, 0.2)'}}>
              <div className="bg-white h-2 rounded-full" style={{width: '57%'}}></div>
            </div>
          </div>
          
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">OVERVIEW</h2>
            
            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-blue-600 bg-blue-50 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="text-sm font-medium">Dashboard</span>
              </button>
              
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="text-sm">Quick Scan</span>
              </button>
            </div>
          </div>
          
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">CONTENT PROTECTION</h2>
            
            <div className="mt-3 space-y-1">
              <Link href="/register" className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span className="text-sm">Register Content</span>
              </Link>
              
              <button className="w-full flex items-center justify-between px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                  <span className="text-sm">My Library</span>
                </div>
                <span className="text-xs font-medium text-gray-500 bg-gray-200 px-2 py-0.5 rounded">127</span>
              </button>
              
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
                </svg>
                <span className="text-sm">Semantic Fingerprints</span>
              </button>
            </div>
          </div>
          
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">MONITORING</h2>
            
            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="text-sm">Content Scanner</span>
              </button>
              
              <button className="w-full flex items-center justify-between px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <span className="text-sm">Potential Matches</span>
                </div>
                <span className="text-xs font-semibold text-yellow-800 bg-yellow-400 px-2 py-0.5 rounded-full">7</span>
              </button>
              
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <span className="text-sm">Watch Lists</span>
              </button>
            </div>
          </div>
          
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">LEGAL ACTIONS</h2>
            
            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center justify-between px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <div className="flex items-center gap-3">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                  </svg>
                  <span className="text-sm">Active Disputes</span>
                </div>
                <span className="text-xs font-semibold text-white bg-red-600 px-2 py-0.5 rounded-full">3</span>
              </button>
              
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm">Evidence Packages</span>
              </button>
              
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
                <span className="text-sm">Blockchain Records</span>
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
          <div className="flex flex-col md:flex-row md:items-start gap-4 md:gap-6 mb-8">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Content Protection Dashboard</h1>
              <p className="text-gray-600 text-sm">
                Monitor your content, track potential copycats, and protect your creative work
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row items-stretch gap-3">
              <Link href="/register" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-3">
                <span className="text-xl font-light">+</span>
                <span className="font-medium">Register New Content</span>
              </Link>
              
              <button className="bg-gray-200 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="font-medium">Quick Scan</span>
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {/* Protected Content */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="w-14 h-14 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-green-600">+12% this month</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">127</div>
              <div className="text-sm text-gray-600">Protected Content</div>
            </div>
            
            {/* Potential Matches */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="w-14 h-14 bg-yellow-50 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-7 h-7 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-red-600">+3 new</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">7</div>
              <div className="text-sm text-gray-600">Potential Matches</div>
            </div>
            
            {/* Active Disputes */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="w-14 h-14 bg-red-50 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-green-600">2 resolved</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">3</div>
              <div className="text-sm text-gray-600">Active Disputes</div>
            </div>
            
            {/* Total Recovered */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="w-14 h-14 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span className="text-sm font-medium text-green-600">$2,450 recovered</span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">$8,900</div>
              <div className="text-sm text-gray-600">Total Recovered</div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">
            {/* Protection Activity Chart */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 lg:col-span-3">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-gray-900">Protection Activity</h2>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setTimeRange('7')}
                    className={`px-3 py-1 text-sm rounded ${timeRange === '7' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'}`}
                  >
                    7 days
                  </button>
                  <button 
                    onClick={() => setTimeRange('30')}
                    className={`px-3 py-1 text-sm rounded ${timeRange === '30' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'}`}
                  >
                    30 days
                  </button>
                  <button 
                    onClick={() => setTimeRange('90')}
                    className={`px-3 py-1 text-sm rounded ${timeRange === '90' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'}`}
                  >
                    90 days
                  </button>
                </div>
              </div>
              
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={activityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#6B7280"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis 
                    stroke="#6B7280"
                    style={{ fontSize: '12px' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'white', 
                      border: '1px solid #E5E7EB',
                      borderRadius: '8px',
                      fontSize: '12px'
                    }}
                  />
                  <Legend 
                    wrapperStyle={{ fontSize: '12px' }}
                    iconType="line"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="contentRegistered" 
                    stroke="#3B82F6" 
                    strokeWidth={2}
                    name="Content Registered"
                    dot={{ fill: '#3B82F6', r: 4 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="matchesFound" 
                    stroke="#EF4444" 
                    strokeWidth={2}
                    name="Matches Found"
                    dot={{ fill: '#EF4444', r: 4 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="disputesFiled" 
                    stroke="#F59E0B" 
                    strokeWidth={2}
                    name="Disputes Filed"
                    dot={{ fill: '#F59E0B', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            {/* Semantic Match Distribution Chart */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 lg:col-span-2">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-gray-900">Semantic Match Distribution</h2>
                <button className="p-2 hover:bg-gray-100 rounded">
                  <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
              </div>
              
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={matchDistributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {matchDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'white', 
                      border: '1px solid #E5E7EB',
                      borderRadius: '8px',
                      fontSize: '12px'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Quick Actions</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Register Content */}
              <Link href="/register" className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-blue-400 hover:bg-blue-50 transition-all text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div className="font-semibold text-gray-900 mb-2">Register Content</div>
                <div className="text-sm text-gray-600">Upload and protect new content</div>
              </Link>
              
              {/* Quick Scan */}
              <Link href="/compare" className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-yellow-400 hover:bg-yellow-50 transition-all text-center">
                <div className="w-16 h-16 bg-yellow-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <div className="font-semibold text-gray-900 mb-2">Quick Scan</div>
                <div className="text-sm text-gray-600">Check for potential matches</div>
              </Link>
              
              {/* File Dispute */}
              <Link href="/dispute" className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-red-400 hover:bg-red-50 transition-all text-center">
                <div className="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                  </svg>
                </div>
                <div className="font-semibold text-gray-900 mb-2">File Dispute</div>
                <div className="text-sm text-gray-600">Start legal action process</div>
              </Link>
              
              {/* View Reports */}
              <button className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-green-400 hover:bg-green-50 transition-all text-center">
                <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div className="font-semibold text-gray-900 mb-2">View Reports</div>
                <div className="text-sm text-gray-600">Detailed analytics dashboard</div>
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Recent Matches Found */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-gray-900">Recent Matches Found</h2>
                <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  View all
                </button>
              </div>
              
              <div className="space-y-3">
                {/* High Similarity Match */}
                <div className="bg-red-50 border border-red-100 rounded-lg p-4">
                  <div className="flex gap-3">
                    <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <h3 className="font-semibold text-gray-900">High Similarity Match</h3>
                        <span className="text-sm font-semibold text-red-600 whitespace-nowrap">94% match</span>
                      </div>
                      <p className="text-sm text-gray-700 mb-2">Your "Life Paths Choice" video concept detected on TikTok</p>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>2 hours ago</span>
                        <span>•</span>
                        <span>@creativecopy_user</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Medium Similarity Match */}
                <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-4">
                  <div className="flex gap-3">
                    <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <h3 className="font-semibold text-gray-900">Medium Similarity Match</h3>
                        <span className="text-sm font-semibold text-yellow-600 whitespace-nowrap">78% match</span>
                      </div>
                      <p className="text-sm text-gray-700 mb-2">Similar narrative structure found in Instagram Reel</p>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>6 hours ago</span>
                        <span>•</span>
                        <span>@inspiration_hub</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Low Similarity Match */}
                <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
                  <div className="flex gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <h3 className="font-semibold text-gray-900">Low Similarity Match</h3>
                        <span className="text-sm font-semibold text-blue-600 whitespace-nowrap">45% match</span>
                      </div>
                      <p className="text-sm text-gray-700 mb-2">Thematic overlap detected in YouTube video</p>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>1 day ago</span>
                        <span>•</span>
                        <span>@motivational_content</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* System Alerts */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-gray-900">System Alerts</h2>
                <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Mark all as read
                </button>
              </div>
              
              <div className="space-y-4">
                {/* Dispute Resolution Complete */}
                <div className="flex gap-3 pb-4 border-b border-gray-100">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 mb-1">Dispute Resolution Complete</h3>
                    <p className="text-sm text-gray-600 mb-2">Case #DR-2024-0156 resolved in your favor</p>
                    <span className="text-xs text-gray-500">30 minutes ago</span>
                  </div>
                </div>
                
                {/* Semantic Fingerprint Generated */}
                <div className="flex gap-3 pb-4 border-b border-gray-100">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 mb-1">Semantic Fingerprint Generated</h3>
                    <p className="text-sm text-gray-600 mb-2">"Morning Routine Transformation" successfully registered</p>
                    <span className="text-xs text-gray-500">2 hours ago</span>
                  </div>
                </div>
                
                {/* Scan Limit Warning */}
                <div className="flex gap-3">
                  <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 mb-1">Scan Limit Warning</h3>
                    <p className="text-sm text-gray-600 mb-2">You've used 2,847 of 5,000 monthly scans</p>
                    <span className="text-xs text-gray-500">4 hours ago</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Protected Content Library */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Protected Content Library</h2>
              <div className="flex gap-2">
                <button className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                  </svg>
                  Filter
                </button>
                <button className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                  Sort
                </button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Content</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Type</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Registered</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Matches Found</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Row 1 */}
                  <tr className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-3">
                        <img
                          src="https://images.unsplash.com/photo-1502014822147-1aedfb0676e0?w=100&h=100&fit=crop"
                          alt="Situational Awareness"
                          className="w-10 h-10 rounded-lg object-cover"
                        />
                        <div>
                          <div className="font-semibold text-gray-900">Situational Awareness</div>
                          <div className="text-sm text-gray-500">AI Timeline Essay</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        Essay
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-700">Jun 1st, 2024</td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-800">
                        1 Medium
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Protected
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Details
                      </button>
                    </td>
                  </tr>
                  
                  {/* Row 2 */}
                  <tr className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-3">
                        <img
                          src="https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=100&h=100&fit=crop"
                          alt="My K-pop Secret"
                          className="w-10 h-10 rounded-lg object-cover"
                        />
                        <div>
                          <div className="font-semibold text-gray-900">My K-pop Secret</div>
                          <div className="text-sm text-gray-500">Radish Fiction Novel</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center justify-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Mini-Novel
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-700">Oct 12, 2022</td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-red-100 text-red-800">
                        3 High
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Protected
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Details
                      </button>
                    </td>
                  </tr>
                  
                  {/* Row 3 */}
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-3">
                        <img 
                          src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=100&h=100&fit=crop" 
                          alt="Creative Entrepreneurship Guide" 
                          className="w-10 h-10 rounded-lg object-cover"
                        />
                        <div>
                          <div className="font-semibold text-gray-900">Creative Entrepreneurship Guide</div>
                          <div className="text-sm text-gray-500">Business strategy framework</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        Course
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-700">Oct 8, 2024</td>
                    <td className="py-4 px-4">
                      <span className="text-sm text-gray-700">0</span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Protected
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Details
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Blockchain Verification Status */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Blockchain Verification Status</h2>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                View on Explorer
              </a>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Verified */}
              <div className="bg-green-50 border border-green-100 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-green-600">Verified</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">124</div>
                <div className="text-sm text-gray-600">Confirmed Records</div>
              </div>
              
              {/* Pending */}
              <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-yellow-600">Pending</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">3</div>
                <div className="text-sm text-gray-600">Awaiting Confirmation</div>
              </div>
              
              {/* Active */}
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-blue-600">Active</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">2.4 ETH</div>
                <div className="text-sm text-gray-600">Gas Fees Paid</div>
              </div>
              
              {/* Unique */}
              <div className="bg-purple-50 border border-purple-100 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-purple-600">Unique</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">127</div>
                <div className="text-sm text-gray-600">Unique Fingerprints</div>
              </div>
            </div>
          </div>
          
          {/* Active Dispute Management */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Active Dispute Management</h2>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2">
                <span className="text-lg font-light">+</span>
                <span className="font-medium">File New Dispute</span>
              </button>
            </div>
            
            <div className="space-y-4">
              {/* Dispute 1 - High Priority */}
              <div className="bg-red-50 border border-red-100 rounded-lg p-6 relative">
                <span className="absolute top-4 right-4 inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-red-600 text-white">
                  High Priority
                </span>
                
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 mb-1">Case #DR-2024-0158</h3>
                    <p className="text-gray-700 mb-4">Life Paths Choice - TikTok Copy</p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <div className="text-xs text-gray-600 mb-1">SIMILARITY SCORE</div>
                        <div className="text-2xl font-bold text-red-600">94%</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">PLATFORM</div>
                        <div className="text-sm font-medium text-gray-900">TikTok</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">FILED DATE</div>
                        <div className="text-sm font-medium text-gray-900">Oct 21, 2024</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">STATUS</div>
                        <div className="text-sm font-semibold text-yellow-600">Under Review</div>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-2">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                        View Evidence Package
                      </button>
                      <button className="bg-white text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors border border-gray-300 text-sm font-medium">
                        Update Status
                      </button>
                      <button className="text-blue-600 hover:text-blue-700 px-4 py-2 text-sm font-medium">
                        View Blockchain Record
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Dispute 2 - Medium Priority */}
              <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-6 relative">
                <span className="absolute top-4 right-4 inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-yellow-500 text-white">
                  Medium Priority
                </span>
                
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900 mb-1">Case #DR-2024-0155</h3>
                    <p className="text-gray-700 mb-4">Morning Routine - Instagram Reel</p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <div className="text-xs text-gray-600 mb-1">SIMILARITY SCORE</div>
                        <div className="text-2xl font-bold text-yellow-600">78%</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">PLATFORM</div>
                        <div className="text-sm font-medium text-gray-900">Instagram</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">FILED DATE</div>
                        <div className="text-sm font-medium text-gray-900">Oct 18, 2024</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">STATUS</div>
                        <div className="text-sm font-semibold text-blue-600">In Progress</div>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-2">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                        View Evidence Package
                      </button>
                      <button className="bg-white text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors border border-gray-300 text-sm font-medium">
                        Update Status
                      </button>
                      <button className="text-blue-600 hover:text-blue-700 px-4 py-2 text-sm font-medium">
                        View Blockchain Record
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* AI-Powered Insights */}
          <div className="bg-gradient-to-br from-purple-100 via-purple-200 to-blue-900 rounded-lg p-6 mb-8 border border-black">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-1">AI-Powered Insights</h2>
                <p className="text-gray-700">Smart recommendations based on your content patterns</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Trend Alert */}
              <div className="bg-white rounded-lg p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900">Trend Alert</h3>
                </div>
                <p className="text-sm text-gray-700 mb-4">
                  Your "Life Paths" concept is trending. Consider registering similar variations to maximize protection.
                </p>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Explore Variations →
                </a>
              </div>
              
              {/* Protection Gap */}
              <div className="bg-white rounded-lg p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900">Protection Gap</h3>
                </div>
                <p className="text-sm text-gray-700 mb-4">
                  You have 15 unprotected pieces of content that share similar themes with your registered works.
                </p>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Review Content →
                </a>
              </div>
              
              {/* Optimization Tip */}
              <div className="bg-white rounded-lg p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900">Optimization Tip</h3>
                </div>
                <p className="text-sm text-gray-700 mb-4">
                  Your semantic fingerprints could be strengthened by adding more character depth analysis.
                </p>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Learn More →
                </a>
              </div>
            </div>
          </div>
          
          {/* Protection Performance */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Protection Performance</h2>
              <select className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500">
                <option>Last 30 days</option>
                <option>Last 60 days</option>
                <option>Last 90 days</option>
              </select>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Detection Accuracy Over Time */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Detection Accuracy Over Time</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <AreaChart data={[
                    { week: 'Week 1', accuracy: 87 },
                    { week: 'Week 2', accuracy: 91 },
                    { week: 'Week 3', accuracy: 94 },
                    { week: 'Week 4', accuracy: 96 },
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis 
                      dataKey="week" 
                      stroke="#6B7280"
                      style={{ fontSize: '12px' }}
                    />
                    <YAxis 
                      stroke="#6B7280"
                      style={{ fontSize: '12px' }}
                      domain={[80, 100]}
                      label={{ value: 'Accuracy %', angle: -90, position: 'insideLeft', style: { fontSize: '12px' } }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'white', 
                        border: '1px solid #E5E7EB',
                        borderRadius: '8px',
                        fontSize: '12px'
                      }}
                    />
                    <defs>
                      <linearGradient id="accuracyGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10B981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <Area 
                      type="monotone" 
                      dataKey="accuracy" 
                      stroke="#10B981" 
                      strokeWidth={2}
                      dot={{ fill: '#10B981', r: 4 }}
                      fill="url(#accuracyGradient)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              
              {/* Response Time Metrics */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Response Time Metrics</h3>
                <div className="space-y-6">
                  <div className="flex items-center justify-between pb-4 border-b border-gray-200">
                    <div>
                      <div className="font-semibold text-gray-900 mb-1">Average Detection Time</div>
                      <div className="text-sm text-gray-600">Time to identify potential matches</div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">2.3h</div>
                      <div className="text-xs text-green-600 flex items-center justify-end gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        15% from last month
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between pb-4 border-b border-gray-200">
                    <div>
                      <div className="font-semibold text-gray-900 mb-1">Evidence Generation</div>
                      <div className="text-sm text-gray-600">Time to compile dispute package</div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">45min</div>
                      <div className="text-xs text-green-600 flex items-center justify-end gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        8% from last month
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-gray-900 mb-1">Resolution Rate</div>
                      <div className="text-sm text-gray-600">Successfully resolved disputes</div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">87%</div>
                      <div className="text-xs text-green-600 flex items-center justify-end gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                        </svg>
                        3% from last month
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
