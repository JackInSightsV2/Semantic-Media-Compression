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
 * @fingerprint SH:JI2:e7b0d3c6f9a2e5c8b1d4f7a0c3e6b9d2
 */

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  getDisputeOptions,
  createDispute,
  getDisputeDetails,
  getActiveDisputes,
  type DisputeOptions,
} from '@/lib/api';

export default function DisputePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [originalIP, setOriginalIP] = useState('');
  const [suspectedIP, setSuspectedIP] = useState('');
  const [filing, setFiling] = useState(false);
  const [filed, setFiled] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [disputeOptions, setDisputeOptions] = useState<DisputeOptions | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notes, setNotes] = useState('');

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

  // Load dispute options on mount
  useEffect(() => {
    getDisputeOptions()
      .then(setDisputeOptions)
      .catch((err) => {
        console.error('Failed to load dispute options:', err);
        setError('Failed to load dispute options');
      });
  }, []);

  // Reset suspected IP when original IP changes
  useEffect(() => {
    setSuspectedIP('');
  }, [originalIP]);

  // Get suspected options from backend
  const suspectedOptions = disputeOptions
    ? disputeOptions.matches
        .filter((match) => match.asset_id === originalIP || !originalIP)
        .map((match) => ({
          value: match.source_reference,
          label: `${match.source_reference} (${Math.round(match.similarity_overall * 100)}% similar)`,
          similarity: `${Math.round(match.similarity_overall * 100)}%`,
          isHigh: match.risk_level === 'high',
        }))
    : [];
  
  async function handleFileDispute() {
    if (!originalIP || !suspectedIP) return;

    setFiling(true);
    setError(null);

    try {
      const response = await createDispute({
        asset_id: originalIP,
        suspect_reference: suspectedIP,
        notes: notes || undefined,
      });

      setResult({
        disputeId: response.dispute.id,
        evidenceIPFS: response.dispute.evidence_cid,
        txHash: response.dispute.tx_hash,
        timestamp: response.dispute.created_at,
        status: response.dispute.status,
      });

      setFiled(true);
    } catch (err: any) {
      setError(err.message || 'Failed to create dispute');
      console.error('Dispute creation error:', err);
    } finally {
      setFiling(false);
    }
  }
  
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
              <button className="w-full bg-red-600 hover:bg-red-700 text-white rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
                </svg>
                <span className="text-sm font-medium">File New Dispute</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm">Upload Evidence</span>
              </button>

              <button className="w-full text-gray-700 hover:bg-gray-100 rounded-lg px-3 py-2 flex items-center gap-3 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <span className="text-sm">View Similar Cases</span>
              </button>
            </div>
          </div>

          {/* Dispute Management */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">DISPUTE MANAGEMENT</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <span className="text-sm">My Disputes</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm">Pending Review</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm">Resolved Cases</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span className="text-sm">Dismissed Cases</span>
              </button>
            </div>
          </div>

          {/* Evidence & Documentation */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">EVIDENCE & DOCUMENTATION</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span className="text-sm">Evidence Library</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="text-sm">Similarity Reports</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="text-sm">Quick Compare</span>
              </button>
            </div>
          </div>

          {/* Help & Resources */}
          <div className="mt-6">
            <h2 className="text-xs font-bold text-gray-700">HELP & RESOURCES</h2>

            <div className="mt-3 space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span className="text-sm">Dispute Guidelines</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm">FAQs</span>
              </button>

              <button className="w-full flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <span className="text-sm">Contact Support</span>
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
              <span>Back</span>
            </Link>

            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">File IP Dispute</h1>
              <p className="text-gray-600 text-sm">
                Report potential intellectual property violations to Story Protocol
              </p>
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
              )}
            </div>
            {/* Step 1: Select IP Assets */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/documents.jpg)' }}></div>
              <div className="flex items-center gap-3 mb-6 relative z-10">
                <div className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 bg-red-600">
                  <span className="text-white font-bold text-lg">1</span>
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Select IP Assets</h2>
              </div>
              
              <div className="space-y-6 relative z-10">
                <div>
                  <label className="block font-semibold text-gray-700 mb-2">
                    Original IP Asset:
                  </label>
                  <select
                    value={originalIP}
                    onChange={(e) => setOriginalIP(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-white text-gray-900"
                    disabled={filing || filed || !disputeOptions}
                  >
                    <option value="">Select your registered IP...</option>
                    {disputeOptions?.assets.map((asset) => (
                      <option key={asset.id} value={asset.id}>
                        {asset.title} ({asset.status})
                      </option>
                    ))}
                  </select>
                  <p className="text-sm text-gray-500 mt-2">Select the IP asset you own that has been plagiarized</p>
                </div>
                
                <div>
                  <label className="block font-semibold text-gray-700 mb-2">
                    Suspected Plagiarism IP Asset:
                  </label>
                  <select 
                    value={suspectedIP}
                    onChange={(e) => setSuspectedIP(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-white text-gray-900"
                    disabled={filing || filed || !originalIP}
                  >
                    <option value="">
                      {originalIP ? 'Select suspected copycat...' : 'First select your original IP asset'}
                    </option>
                    {suspectedOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                  <p className="text-sm text-gray-500 mt-2">
                    {originalIP
                      ? 'Select the IP asset that appears to be plagiarizing your work'
                      : 'Please select your original IP asset first'}
                  </p>
                </div>

                <div>
                  <label className="block font-semibold text-gray-700 mb-2">
                    Notes (Optional):
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-white text-gray-900"
                    rows={4}
                    placeholder="Add any additional notes about this dispute..."
                    disabled={filing || filed}
                  />
                </div>
              </div>
            </div>
            
            {/* Submit Button */}
            {!filed && (
              <div className="text-center mb-8">
                <button 
                  onClick={handleFileDispute}
                  disabled={!originalIP || !suspectedIP || filing || filed}
                  className="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-12 py-4 rounded-lg font-medium transition-colors text-lg"
                >
                  {filing ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Filing Dispute...
                    </span>
                  ) : (
                    'Submit Dispute to Story Protocol'
                  )}
                </button>
              </div>
            )}

            {/* Loading State */}
            {filing && (
              <div className="bg-red-50 border-2 border-red-200 rounded-lg p-8 text-center">
                <div className="inline-block animate-pulse mb-4">
                  <div className="text-5xl">⚖️</div>
                </div>
                <h3 className="text-xl font-semibold text-red-700 mb-2">
                  Submitting Dispute On-Chain...
                </h3>
                <p className="text-sm text-gray-600 mb-1">
                  Uploading evidence to IPFS and minting dispute on Story Protocol
                </p>
                <p className="text-xs text-gray-500">
                  This may take a few moments...
                </p>
              </div>
            )}

            {/* Success Card - Contract Information */}
            {filed && result && (
              <div className="bg-white rounded-lg border-2 border-green-500 p-6 mb-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-5" style={{ backgroundImage: 'url(/blockchain.jpg)' }}></div>
                
                <div className="relative z-10">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                      <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-green-700">Dispute Submitted Successfully!</h3>
                      <p className="text-gray-600 text-sm">Your dispute has been minted on-chain to Story Protocol</p>
                    </div>
                  </div>

                  {/* Transaction Details */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-sm font-semibold text-gray-700 mb-2">Dispute ID</div>
                      <div className="font-mono text-xs text-gray-900 break-all">{result.disputeId}</div>
                    </div>

                    {result.status && (
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="text-sm font-semibold text-gray-700 mb-2">Status</div>
                        <div className="font-mono text-xs text-gray-900">{result.status}</div>
                      </div>
                    )}

                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-sm font-semibold text-gray-700 mb-2">Evidence IPFS Hash</div>
                      <div className="font-mono text-xs text-gray-900 break-all">{result.evidenceIPFS}</div>
                    </div>

                    <div className="bg-gray-50 rounded-lg p-4">
                      <div className="text-sm font-semibold text-gray-700 mb-2">Transaction Hash</div>
                      <div className="font-mono text-xs text-gray-900 break-all">{result.txHash}</div>
                    </div>
                  </div>

                  {/* Dispute Metadata */}
                  {result.timestamp && (
                    <div className="border-t border-gray-200 pt-6">
                      <h4 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Dispute Information
                      </h4>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-blue-50 rounded-lg p-4">
                          <div className="text-sm font-semibold text-gray-700 mb-1">Created</div>
                          <div className="text-gray-900">
                            {new Date(result.timestamp).toLocaleString()}
                          </div>
                        </div>

                        {result.evidenceIPFS && (
                          <div className="bg-blue-50 rounded-lg p-4">
                            <div className="text-sm font-semibold text-gray-700 mb-1">Evidence IPFS</div>
                            <div className="text-gray-900 font-mono text-xs break-all">{result.evidenceIPFS}</div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Status Badge */}
                  <div className="mt-6 flex items-center justify-between">
                    <div>
                      <span className="text-sm font-semibold text-gray-700 mr-2">Status:</span>
                      <span className="inline-block px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold">
                        Pending Review
                      </span>
                    </div>
                    <Link
                      href="/"
                      className="text-blue-600 hover:text-blue-700 font-semibold flex items-center gap-1"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                      </svg>
                      Return to Dashboard
                    </Link>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

