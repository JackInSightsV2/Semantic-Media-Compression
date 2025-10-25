/**
 * Copyright 2024-2025 Stephen Henry JackInSightsV2
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * @author Stephen Henry JackInSightsV2
 * @fingerprint SH:JI2:a5c8e2b9f6d3a7c0e4f7b2d5a8c1e4f7
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

// Import comparison data and semantic data
import comparisonData from '@/demo-data/semantic_comparison_report.json';
import mykpopsecret from '@/demo-data/mykpopsecret.json';

type ScanStep = 'upload' | 'scanning' | 'scanned';
type UploadedFileType = 'situational_awareness' | 'mykpopsecret' | 'unknown';

export default function QuickScanPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Scanning flow state
  const [currentStep, setCurrentStep] = useState<ScanStep>('upload');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [detectedFileType, setDetectedFileType] = useState<UploadedFileType>('unknown');
  const [urlToScan, setUrlToScan] = useState('');
  const [scanSourceLabel, setScanSourceLabel] = useState<string>('');

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

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      setScanSourceLabel(file.name);
      
      // Detect file type based on filename
      const filename = file.name.toLowerCase();
      if (filename.includes('mykpopsecret')) {
        setDetectedFileType('mykpopsecret');
      } else if (filename.includes('situational') || filename.includes('awareness')) {
        setDetectedFileType('situational_awareness');
      } else {
        // Default to situational_awareness for unknown files
        setDetectedFileType('situational_awareness');
      }
      
      setCurrentStep('scanning');
      
      // Mock scanning text file (10 seconds)
      setTimeout(() => {
        setCurrentStep('scanned');
      }, 10000);
    }
  };

  // Handle URL scan (mock)
  const handleUrlScan = () => {
    const trimmed = urlToScan.trim().replace(/^@+/, '');
    if (!trimmed) return;
    try {
      // Basic validation
      // eslint-disable-next-line no-new
      new URL(trimmed);
    } catch {
      return;
    }
    setUploadedFile(null);
    setScanSourceLabel(trimmed);
    // Simple platform-based mock detection
    const lower = trimmed.toLowerCase();
    if (lower === 'https://www.youtube.com/watch?v=gzjzvosvdjm') {
      // Hard-map this specific URL to situational awareness mock
      setDetectedFileType('situational_awareness');
    } else if (lower.includes('kpop')) {
      setDetectedFileType('mykpopsecret');
    } else {
      setDetectedFileType('situational_awareness');
    }
    setCurrentStep('scanning');
    setTimeout(() => setCurrentStep('scanned'), 10000);
  };

  // Handle reset for another scan
  const handleReset = () => {
    setCurrentStep('upload');
    setUploadedFile(null);
    setDetectedFileType('unknown');
    setUrlToScan('');
    setScanSourceLabel('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  // Get appropriate semantic data based on detected file type
  const getSemanticData = () => {
    if (detectedFileType === 'mykpopsecret') {
      return Array.isArray(mykpopsecret) ? mykpopsecret[0] : mykpopsecret;
    }
    // Default to situational_awareness comparison data
    return comparisonData;
  };
  
  const semanticData = getSemanticData();
  const isUrlSource = !uploadedFile && !!scanSourceLabel && scanSourceLabel.startsWith('http');
  const normalizedUrl = (scanSourceLabel || '').replace(/^@+/, '');
  const isNotebookLMYouTube = isUrlSource && normalizedUrl.toLowerCase() === 'https://www.youtube.com/watch?v=gzjzvosvdjm';
  const urlPlatform = isUrlSource
    ? (normalizedUrl.includes('youtube.com') || normalizedUrl.includes('youtu.be'))
      ? 'YouTube'
      : normalizedUrl.includes('tiktok.com')
      ? 'TikTok'
      : normalizedUrl.includes('instagram.com')
      ? 'Instagram'
      : 'Web'
    : '';

  return (
    <div className="h-screen bg-gray-50 overflow-hidden flex flex-col">
      <header className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-[60]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8 flex-1">
            <div className="flex items-center gap-3">
              <h1 className="text-xl md:text-2xl font-bold text-gray-900 flex items-center gap-2">
                Semantic IP Protection + Story 
                <img src="/symbol-dark.png" alt="Story Protocol" className="h-6 md:h-8 inline-block" />
              </h1>
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="text-sm font-medium">New Scan</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                <span className="text-sm">Upload File</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="text-sm">Batch Scan</span>
              </button>
            </div>
          </div>

          {/* Scan Options */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">SCAN OPTIONS</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm">Text Document</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span className="text-sm">Video Content</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className="text-sm">Image/Art</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                </svg>
                <span className="text-sm">Audio Track</span>
              </button>
            </div>
          </div>

          {/* Scan History */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">SCAN HISTORY</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm">Recent Scans</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
                <span className="text-sm">Saved Results</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-sm">Scan Analytics</span>
              </button>
            </div>
          </div>

          {/* Settings */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">SETTINGS</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                </svg>
                <span className="text-sm">Scan Preferences</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="text-sm">Notifications</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm">Help & Support</span>
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

        <main className="flex-1 p-4 md:p-8 overflow-y-auto relative">
          <div className="hidden lg:block fixed inset-0 bg-cover bg-center bg-no-repeat opacity-5 pointer-events-none" style={{ backgroundImage: 'url(/graph1.jpg)', left: 'auto', right: 0, width: 'calc(100% - 256px)' }}></div>
          <div className="lg:hidden fixed inset-0 bg-cover bg-center bg-no-repeat opacity-5 pointer-events-none" style={{ backgroundImage: 'url(/graph1.jpg)' }}></div>
          <div className="relative z-10">
            <Link href="/" className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span>Return to Dashboard</span>
            </Link>

            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Semantic IP - Quick Scan</h1>
              <p className="text-gray-600 text-sm">
                Scan for protected IP that has been registered on the Story Blockchain
              </p>
            </div>

            {/* Upload Content Card */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/documents.jpg)' }}></div>
              <div className="flex items-center gap-3 mb-6 relative z-10">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  currentStep !== 'upload' ? 'bg-green-600' : 'bg-blue-600'
                }`}>
                  {currentStep !== 'upload' ? (
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="text-white font-bold text-lg">1</span>
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Upload Content to Scan</h2>
              </div>

              {currentStep === 'upload' ? (
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 md:p-8 lg:p-10 hover:border-blue-400 transition-colors relative z-10">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
                    {/* File Upload Card */}
                    <div className="rounded-lg border border-gray-200 p-6 text-center bg-white/60">
                      <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        accept=".txt"
                        className="hidden"
                      />
                      <div className="flex flex-col items-center">
                        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                          <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                          </svg>
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 mb-2">Upload Content to Scan</h3>
                        <p className="text-gray-600 mb-6">Select a text file to scan for protected IP</p>
                        <button
                          onClick={() => fileInputRef.current?.click()}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors"
                        >
                          Choose File
                        </button>
                        <p className="text-sm text-gray-500 mt-4">Supported format: TXT</p>
                      </div>
                    </div>

                    {/* URL Scan Card */}
                    <div className="rounded-lg border border-gray-200 p-6 bg-white/60">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                          <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-gray-900 leading-none">Scan from URL</h3>
                          <p className="text-gray-600 text-sm mt-1">Paste a link (YouTube, TikTok, Instagram)</p>
                        </div>
                      </div>
                      <div className="space-y-3">
                        <input
                          type="url"
                          value={urlToScan}
                          onChange={(e) => {
                            const next = e.target.value;
                            if (next.trim() === '$$yt') {
                              setUrlToScan('https://www.youtube.com/watch?v=GzjZVoSvdJM');
                            } else {
                              setUrlToScan(next);
                            }
                          }}
                          placeholder="https://youtu.be/... or https://www.tiktok.com/... or https://www.instagram.com/p/..."
                          className="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-purple-500 focus:bg-white"
                        />
                        <div className="flex items-center justify-between">
                          <button
                            onClick={handleUrlScan}
                            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                            disabled={!urlToScan.trim()}
                          >
                            Scan URL
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : currentStep === 'scanning' ? (
                <div className="bg-blue-50 rounded-lg p-8 text-center relative z-10">
                  <div className="flex flex-col items-center">
                    <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4 animate-pulse">
                      <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Scanning Content...</h3>
                    <p className="text-gray-600 mb-1">Generating a semantic version of the media for comparison</p>
                    <p className="text-sm text-gray-500">This may take a few moments...</p>
                  </div>
                </div>
              ) : (
                <div className="bg-gradient-to-r from-green-50/60 to-blue-50/60 rounded-lg border border-green-100 p-6 relative z-10">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center flex-shrink-0">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>

                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{scanSourceLabel || uploadedFile?.name || 'situational_awareness_semantic.txt'}</h3>
                      <p className="text-gray-600 mb-4">Scan completed successfully</p>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <span className="text-gray-700 font-medium text-sm">File Type:</span>
                          <p className="text-gray-900">{uploadedFile ? 'Text Document' : 'URL'}</p>
                        </div>
                        <div>
                          <span className="text-gray-700 font-medium text-sm">File Size:</span>
                          <p className="text-gray-900">{uploadedFile ? Math.round(uploadedFile.size / 1024) + ' KB' : '-'}</p>
                        </div>
                        <div>
                          <span className="text-gray-700 font-medium text-sm">Scan Date:</span>
                          <p className="text-gray-900">{new Date().toLocaleDateString()}</p>
                        </div>
                        <div>
                          <span className="text-gray-700 font-medium text-sm">Status:</span>
                          <p className="text-gray-900">Complete</p>
                        </div>
                        {isUrlSource && (
                          <div className="col-span-2">
                            <span className="text-gray-700 font-medium text-sm">Source URL:</span>
                            <p className="text-gray-900 break-all">{normalizedUrl}</p>
                          </div>
                        )}
                      </div>
                    </div>

                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-600 text-white">
                      ✓ Scanned
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Semantic Fingerprint Section - Only show after scan is complete */}
            {currentStep === 'scanned' && (
              <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/protected.png)' }}></div>
                <div className="flex items-center gap-3 mb-6 relative z-10">
                  <div className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 bg-green-600">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">Semantic Analysis Results</h2>
                </div>

                {/* Semantic Fingerprint Cards */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6 relative z-10">
                  {/* Card 1: Document Profile */}
                  <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/documents.jpg)' }}></div>
                    <div className="flex items-center gap-2 mb-4 relative z-10">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <h4 className="font-bold text-gray-900">Document Profile</h4>
                    </div>

                    <div className="space-y-3 relative z-10">
                      {detectedFileType === 'mykpopsecret' ? (
                        <>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Document Type</span>
                            <span className="text-gray-600 text-right text-sm">{(semanticData as any).document_metadata?.document_type || 'Fiction Narrative'}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Size</span>
                            <span className="text-gray-600 text-right">{uploadedFile ? Math.round(uploadedFile.size / 1024) : '52'} KB</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Domain</span>
                            <span className="text-gray-600 text-right text-sm">{(semanticData as any).document_metadata?.domain?.split(', ')[0] || 'Fiction'}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Episodes</span>
                            <span className="text-gray-600 text-right">10</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Narrative Style</span>
                            <span className="text-gray-600 text-right text-sm">dual-POV romance drama</span>
                          </div>
                        </>
                      ) : (
                        <>
                          {isUrlSource && (
                            <>
                              <div className="flex justify-between items-start">
                                <span className="text-gray-700 font-medium">Source URL</span>
                                <span className="text-gray-600 text-right break-all text-sm">{normalizedUrl}</span>
                              </div>
                              <div className="flex justify-between items-start">
                                <span className="text-gray-700 font-medium">Platform</span>
                                <span className="text-gray-600 text-right text-sm">{urlPlatform}</span>
                              </div>
                              {isNotebookLMYouTube && (
                                <div className="flex justify-between items-start">
                                  <span className="text-gray-700 font-medium">Description</span>
                                  <span className="text-gray-600 text-right text-sm">NotebookLM podcast of Situational Awareness PDF</span>
                                </div>
                              )}
                            </>
                          )}
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Format</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).document_fingerprint?.target_txt?.format || 'linear_prose'}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Size</span>
                            <span className="text-gray-600 text-right">{Math.round(((semanticData as any).document_fingerprint?.target_txt?.total_size_bytes || 46893) / 1024)} KB</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Chapters</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).document_fingerprint?.target_txt?.chapters || 7}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Subsections</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).document_fingerprint?.target_txt?.subsections || 89}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Narrative Style</span>
                            <span className="text-gray-600 text-right text-sm">{(semanticData as any).document_fingerprint?.target_txt?.narrative_style || 'technical_directive'}</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Card 2: Semantic Elements */}
                  <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/jsoncode.jpg)' }}></div>
                    <div className="flex items-center gap-2 mb-4 relative z-10">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                      </svg>
                      <h4 className="font-bold text-gray-900">Semantic Elements</h4>
                    </div>

                    <div className="space-y-3 relative z-10">
                      {detectedFileType === 'mykpopsecret' ? (
                        <>
                          <div>
                            <div className="text-gray-700 font-medium mb-2">Key Themes</div>
                            <div className="flex flex-wrap gap-2">
                              {((semanticData as any).global_context?.key_themes || []).slice(0, 4).map((theme: string, idx: number) => (
                                <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">{theme}</span>
                              ))}
                            </div>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Total Themes</span>
                            <span className="text-gray-600 text-right">{((semanticData as any).global_context?.key_themes || []).length}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Primary Objectives</span>
                            <span className="text-gray-600 text-right">{((semanticData as any).global_context?.primary_objectives || []).length}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Narrative Arc</span>
                            <span className="text-gray-600 text-right text-sm">{(semanticData as any).global_context?.narrative_arc?.structure || 'complex'}</span>
                          </div>
                        </>
                      ) : (
                        <>
                          <div>
                            <div className="text-gray-700 font-medium mb-2">Core Concepts</div>
                            <div className="flex flex-wrap gap-2">
                              {((semanticData as any).content_coverage?.preserved_elements?.core_concepts?.examples || []).slice(0, 4).map((concept: string, idx: number) => (
                                <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">{concept}</span>
                              ))}
                            </div>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Total Concepts</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).content_coverage?.preserved_elements?.core_concepts?.count || 0}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Key Arguments</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).content_coverage?.preserved_elements?.key_arguments?.count || 0}</span>
                          </div>
                          <div className="flex justify-between items-start">
                            <span className="text-gray-700 font-medium">Quantitative Data</span>
                            <span className="text-gray-600 text-right">{(semanticData as any).content_coverage?.preserved_elements?.quantitative_data?.numbers_preserved || 0} numbers</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Card 3: Fingerprint Summary */}
                  <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/protected.png)' }}></div>
                    <div className="flex items-center gap-2 mb-4 relative z-10">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
                      </svg>
                      <h4 className="font-bold text-gray-900">Fingerprint Summary</h4>
                    </div>

                    <div className="space-y-4 relative z-10">
                      <div>
                        <div className="text-gray-700 font-medium mb-2">Semantic Hash</div>
                        <div className="bg-gray-50 rounded p-3 font-mono text-xs break-all text-gray-700">
                          {detectedFileType === 'mykpopsecret' 
                            ? '0x7f3c9a8e2b1d5647fa9c0e8b3d7a2c5f9e1b4d7a3c6f8e1b'
                            : '0x24dd57dca315180000000000000000000000000000000000'
                          }
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-blue-50 rounded-lg p-4 text-center">
                          <div className="text-3xl font-bold text-blue-600 mb-1">
                            {detectedFileType === 'mykpopsecret' ? '94%' : '96%'}
                          </div>
                          <div className="text-sm text-gray-600">Uniqueness Score</div>
                        </div>
                        <div className="bg-green-50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-green-600 mb-1">
                            {detectedFileType === 'mykpopsecret' ? 'Very High' : 'Very High'}
                          </div>
                          <div className="text-sm text-gray-600">Protection Level</div>
                        </div>
                      </div>

                      <div className="bg-purple-50 rounded-lg p-4 text-center">
                        <div className="text-xl font-bold text-purple-600 mb-1">
                          {detectedFileType === 'mykpopsecret' ? 'Very High' : 'High'}
                        </div>
                        <div className="text-sm text-gray-600">Complexity Score</div>
                        <div className="text-xs text-gray-500 mt-1">
                          {detectedFileType === 'mykpopsecret' 
                            ? '(dual-POV narrative fiction)'
                            : '(strategic policy document)'
                          }
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Card 4: IP Comparison Results */}
                  <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/blockchain.jpg)' }}></div>
                    <div className="flex items-center gap-2 mb-4 relative z-10">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                      <h4 className="font-bold text-gray-900">Registered IP Matches</h4>
                    </div>

                    <div className="space-y-3 relative z-10">
                      {detectedFileType === 'mykpopsecret' ? (
                        <>
                          {/* Match 1: My K-pop Secret (HIGH MATCH) */}
                          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">My K-pop Secret</span>
                              <span className="text-lg font-bold text-red-600">98%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">K-pop Romance Drama Fiction</div>
                            <div className="flex items-center justify-between gap-2">
                              <div className="flex items-center gap-2">
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-red-600 text-white">
                                  HIGH MATCH
                                </span>
                                <span className="text-xs text-red-700">Potential IP Violation</span>
                              </div>
                              <Link href="/dispute" className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-2 hover:border-red-400 hover:bg-red-50 transition-all flex items-center gap-2">
                                <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                                  <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                                  </svg>
                                </div>
                                <div className="flex-1 min-w-0">
                                  <div className="font-semibold text-gray-900 text-xs whitespace-nowrap">File Dispute</div>
                                </div>
                              </Link>
                            </div>
                          </div>

                          {/* Match 2: Situational Awareness */}
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">Situational Awareness</span>
                              <span className="text-lg font-bold text-blue-600">8%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">Strategic Policy Document</div>
                            <div className="flex items-center gap-2">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                                NO MATCH
                              </span>
                              <span className="text-xs text-blue-700">Safe</span>
                            </div>
                          </div>

                          {/* Match 3: Entrepreneurship Guide */}
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">Creative Entrepreneurship</span>
                              <span className="text-lg font-bold text-blue-600">15%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">Business Course</div>
                            <div className="flex items-center gap-2">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                                NO MATCH
                              </span>
                              <span className="text-xs text-blue-700">Safe</span>
                            </div>
                          </div>
                        </>
                      ) : (
                        <>
                          {/* Match 1: Situational Awareness (HIGH MATCH) */}
                          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">Situational Awareness</span>
                              <span className="text-lg font-bold text-red-600">{Math.round(((semanticData as any).semantic_similarity_metrics?.overall_similarity || 0.87) * 100)}%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">Strategic Policy Document</div>
                            <div className="flex items-center justify-between gap-2">
                              <div className="flex items-center gap-2">
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-red-600 text-white">
                                  HIGH MATCH
                                </span>
                                <span className="text-xs text-red-700">Potential IP Violation</span>
                              </div>
                              <Link href="/dispute" className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-2 hover:border-red-400 hover:bg-red-50 transition-all flex items-center gap-2">
                                <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
                                  <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                                  </svg>
                                </div>
                                <div className="flex-1 min-w-0">
                                  <div className="font-semibold text-gray-900 text-xs whitespace-nowrap">File Dispute</div>
                                </div>
                              </Link>
                            </div>
                          </div>

                          {/* Match 2: My K-pop Secret */}
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">My K-pop Secret</span>
                              <span className="text-lg font-bold text-blue-600">12%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">K-pop Romance Drama Fiction</div>
                            <div className="flex items-center gap-2">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                                NO MATCH
                              </span>
                              <span className="text-xs text-blue-700">Safe</span>
                            </div>
                          </div>

                          {/* Match 3: Entrepreneurship Guide */}
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-semibold text-gray-900 text-sm">Creative Entrepreneurship</span>
                              <span className="text-lg font-bold text-blue-600">18%</span>
                            </div>
                            <div className="text-xs text-gray-600 mb-2">Business Course</div>
                            <div className="flex items-center gap-2">
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                                NO MATCH
                              </span>
                              <span className="text-xs text-blue-700">Safe</span>
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                {/* Try Another Scan Section */}
                <div className="flex items-center gap-4 relative z-10">
                  <div className="flex-1 border-t border-gray-300"></div>
                  <button
                    onClick={handleReset}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors whitespace-nowrap"
                  >
                    TRY ANOTHER SCAN
                  </button>
                  <div className="flex-1 border-t border-gray-300"></div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

