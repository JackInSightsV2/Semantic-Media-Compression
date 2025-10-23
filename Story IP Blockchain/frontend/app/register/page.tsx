'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { uploadToIPFS } from '@/blocklibs/ipfs';
import { registerIPAsset } from '@/blocklibs/StoryProtocol';
import { getExplorerUrl, getIPFSUrl, getIPAssetUrl } from '@/blocklibs/utils';
import { useRegisteredContent } from '@/context/RegisteredContentContext';

// Import demo data
import situationalAwareness from '@/demo-data/situational_awareness.json';

type RegistrationStep = 'upload' | 'analyze' | 'build' | 'preview' | 'approved' | 'registered';

export default function RegisterPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Registration flow state
  const [currentStep, setCurrentStep] = useState<RegistrationStep>('upload');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [buildingFingerprint, setBuildingFingerprint] = useState(false);
  const [registering, setRegistering] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const { registerContent } = useRegisteredContent();
  
  const currentData = situationalAwareness;

  // Restore state from sessionStorage on mount (only if coming from view-json)
  useEffect(() => {
    const savedStep = sessionStorage.getItem('registerStep');
    const fromViewJson = sessionStorage.getItem('fromViewJson');
    
    if (savedStep && fromViewJson === 'true') {
      setCurrentStep(savedStep as RegistrationStep);
      // If we're returning to a step after upload, create a mock file
      if (savedStep !== 'upload') {
        const mockFile = new File([''], 'situational_awareness.pdf', { type: 'application/pdf' });
        setUploadedFile(mockFile);
      }
      // Clear the flag after restoring
      sessionStorage.removeItem('fromViewJson');
    }
  }, []);

  // Save state to sessionStorage whenever currentStep changes
  useEffect(() => {
    if (currentStep !== 'upload') {
      sessionStorage.setItem('registerStep', currentStep);
    }
  }, [currentStep]);

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
      // Clear any saved state when starting new upload
      sessionStorage.removeItem('registerStep');
      setUploadedFile(file);
      setCurrentStep('analyze');
      
      // Mock analyzing PDF (2 seconds)
      setTimeout(() => {
        setCurrentStep('build');
      }, 2000);
    }
  };

  // Handle building semantic fingerprint
  const handleBuildFingerprint = () => {
    setBuildingFingerprint(true);
    
    // Mock building fingerprint (10 seconds)
    setTimeout(() => {
      setBuildingFingerprint(false);
      setCurrentStep('preview');
    }, 10000);
  };

  // Handle approving fingerprint
  const handleApproveFingerprint = () => {
    setCurrentStep('approved');
  };

  // Handle blockchain registration
  async function handleRegister() {
    setRegistering(true);
    
    try {
      // TRY REAL BLOCKCHAIN FIRST
      try {
        console.log('📤 Uploading semantic JSON to IPFS...');
        
        // 1. Upload semantic JSON to IPFS
        const ipfsHash = await uploadToIPFS(currentData);
        console.log('✅ Uploaded to IPFS:', ipfsHash);
        
        console.log('⛓️  Registering on Story Protocol...');
        
        // 2. Register on Story Protocol
        const { ipAssetId, txHash, tokenId } = await registerIPAsset({
          name: currentData.document_metadata.title,
          description: currentData.document_metadata.purpose,
          ipfsHash: ipfsHash,
        });
        
        console.log('✅ Registered on Story Protocol!');
        console.log('   IP Asset ID:', ipAssetId);
        console.log('   Token ID:', tokenId);
        console.log('   Transaction Hash:', txHash);
        
        setResult({
          ipAssetId: ipAssetId,
          ipfsHash: ipfsHash,
          txHash: txHash,
          tokenId: tokenId,
          source: 'blockchain', // Mark as real
        });
      } catch (blockchainError) {
        // FALLBACK TO MOCK for demo safety
        console.warn('⚠️ Blockchain failed, using mock data for demo:', blockchainError);
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        setResult({
          ipAssetId: '0x' + Math.random().toString(16).substr(2, 40),
          ipfsHash: 'Qm' + Math.random().toString(36).substr(2, 44),
          txHash: '0x' + Math.random().toString(16).substr(2, 64),
          tokenId: 'N/A',
          source: 'mock', // Mark as fallback
        });
      }
      
      // Register in context so it appears on dashboard
      registerContent('situational-awareness');
      setCurrentStep('registered');
      // Clear saved state when registration is complete
      sessionStorage.removeItem('registerStep');
    } finally {
      setRegistering(false);
    }
  }

  const progressPercentage = 
    currentStep === 'upload' ? 0 :
    currentStep === 'analyze' ? 10 :
    currentStep === 'build' ? 15 :
    currentStep === 'preview' ? 33 :
    currentStep === 'approved' ? 66 :
    currentStep === 'registered' ? 100 : 0;

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

          <div className="absolute bottom-[36px] right-4">
            <button className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          </div>
        </aside>

        <main className="flex-1 p-4 md:p-8 overflow-y-auto relative">
          <div className="fixed inset-0 bg-cover bg-center bg-no-repeat opacity-5 pointer-events-none" style={{ backgroundImage: 'url(/graph1.jpg)', left: 'auto', right: 0, width: 'calc(100% - 256px)' }}></div>
          <div className="relative z-10">
          <Link href="/" className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>Back to Dashboard</span>
          </Link>

          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Register Semantic IP</h1>
            <p className="text-gray-600 text-sm">
              Protect your creative content with blockchain-based intellectual property registration
            </p>
          </div>

          {/* Step 1: Upload Content */}
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
              <h2 className="text-2xl font-bold text-gray-900">Upload Content</h2>
            </div>

            {currentStep === 'upload' ? (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors relative z-10">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept=".pdf,.doc,.docx"
                  className="hidden"
                />
                <div className="flex flex-col items-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Upload Your Content</h3>
                  <p className="text-gray-600 mb-6">Select a PDF or document file to register</p>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors"
                  >
                    Choose File
                  </button>
                  <p className="text-sm text-gray-500 mt-4">Supported formats: PDF, DOC, DOCX</p>
                </div>
              </div>
            ) : currentStep === 'analyze' ? (
              <div className="bg-blue-50 rounded-lg p-8 text-center relative z-10">
                <div className="flex flex-col items-center">
                  <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4 animate-pulse">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Analyzing PDF...</h3>
                  <p className="text-gray-600">Extracting content and metadata</p>
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
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{currentData.document_metadata.title}</h3>
                    <p className="text-gray-600 mb-4">{currentData.document_metadata.purpose}</p>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-gray-700 font-medium text-sm">Document Type:</span>
                        <p className="text-gray-900">{currentData.document_metadata.document_type}</p>
                      </div>
                      <div>
                        <span className="text-gray-700 font-medium text-sm">Domain:</span>
                        <p className="text-gray-900">{currentData.document_metadata.domain.split(', ')[0]}</p>
                      </div>
                      <div>
                        <span className="text-gray-700 font-medium text-sm">Publication Date:</span>
                        <p className="text-gray-900">{currentData.document_metadata.publication_context.date}</p>
                      </div>
                      <div>
                        <span className="text-gray-700 font-medium text-sm">File Name:</span>
                        <p className="text-gray-900">{uploadedFile?.name || 'situational_awareness.pdf'}</p>
                      </div>
                    </div>
                  </div>

                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-600 text-white">
                    ✓ Uploaded
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Step 2: Build & Preview Semantic Fingerprint */}
          {['build', 'preview', 'approved', 'registered'].includes(currentStep) && (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/protected.png)' }}></div>
              <div className="flex items-center gap-3 mb-6 relative z-10">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  ['approved', 'registered'].includes(currentStep) ? 'bg-green-600' : 'bg-blue-600'
                }`}>
                  {['approved', 'registered'].includes(currentStep) ? (
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="text-white font-bold text-lg">2</span>
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Build & Preview Semantic Fingerprint</h2>
              </div>

              {currentStep === 'build' && !buildingFingerprint && (
                <div className="bg-gradient-to-r from-purple-50/60 to-blue-50/60 rounded-lg p-12 text-center relative z-10">
                  <div className="flex flex-col items-center">
                    <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                      <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Ready to Build Semantic IP</h3>
                    <p className="text-gray-600 mb-6">Generate a unique semantic fingerprint for your content</p>
                    <button
                      onClick={handleBuildFingerprint}
                      className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Build Semantic IP
                    </button>
                  </div>
                </div>
              )}

              {buildingFingerprint && (
                <div className="bg-gradient-to-r from-purple-50/60 to-blue-50/60 rounded-lg p-8 text-center relative z-10">
                  <div className="flex flex-col items-center">
                    <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mb-4 animate-pulse">
                      <svg className="w-8 h-8 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Building Semantic Fingerprint...</h3>
                    <p className="text-gray-600 mb-1">LLM analyzing and distilling semantic meaning</p>
                    <p className="text-sm text-gray-500">This may take a few moments...</p>
                  </div>
                </div>
              )}

              {['preview', 'approved', 'registered'].includes(currentStep) && (
                <>
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
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Document Type</span>
                          <span className="text-gray-600 text-right">{currentData.document_metadata.document_type}</span>
                        </div>
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Domain</span>
                          <span className="text-gray-600 text-right text-sm">{currentData.document_metadata.domain}</span>
                        </div>
                        <div>
                          <div className="text-gray-700 font-medium mb-2">Intended Audience</div>
                          <div className="flex flex-wrap gap-2">
                            {currentData.document_metadata.intended_audience.slice(0, 3).map((audience: string, idx: number) => (
                              <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">{audience}</span>
                            ))}
                          </div>
                        </div>
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Publication Date</span>
                          <span className="text-gray-600 text-right">{currentData.document_metadata.publication_context.date}</span>
                        </div>
                      </div>
                    </div>

                    {/* Card 2: Core Thesis & Themes */}
                    <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                      <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/documents.jpg)' }}></div>
                      <div className="flex items-center gap-2 mb-4 relative z-10">
                        <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        <h4 className="font-bold text-gray-900">Core Thesis & Themes</h4>
                      </div>

                      <div className="space-y-3 relative z-10">
                        <div>
                          <div className="text-gray-700 font-medium mb-1">Core Thesis</div>
                          <p className="text-gray-600 text-sm">{currentData.global_context.core_thesis.substring(0, 150)}...</p>
                        </div>
                        <div>
                          <div className="text-gray-700 font-medium mb-2">Key Themes</div>
                          <div className="flex flex-wrap gap-2">
                            {currentData.global_context.key_themes.slice(0, 4).map((theme: string, idx: number) => (
                              <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">{theme}</span>
                            ))}
                          </div>
                        </div>
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Narrative Arc</span>
                          <span className="text-gray-600 text-right text-sm">{currentData.global_context.narrative_arc.structure}</span>
                        </div>
                      </div>
                    </div>

                    {/* Card 3: Semantic Elements */}
                    <div className="bg-white rounded-lg border border-black p-6 relative overflow-hidden">
                      <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/jsoncode.jpg)' }}></div>
                      <div className="flex items-center gap-2 mb-4 relative z-10">
                        <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                        </svg>
                        <h4 className="font-bold text-gray-900">Semantic Elements</h4>
                      </div>

                      <div className="space-y-3 relative z-10">
                        <div>
                          <div className="text-gray-700 font-medium mb-2">Primary Arguments</div>
                          <div className="flex flex-wrap gap-2">
                            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">AGI by ~2027</span>
                            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">intelligence explosion</span>
                            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">industrial mobilization</span>
                          </div>
                        </div>
                        <div>
                          <div className="text-gray-700 font-medium mb-2">Key Concepts</div>
                          <div className="flex flex-wrap gap-2">
                            <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">scaling laws</span>
                            <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">OOMs</span>
                            <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">unhobbling</span>
                            <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm">The Project</span>
                          </div>
                        </div>
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Emotional Tone</span>
                          <span className="text-gray-600 text-right text-sm">urgent, analytical, forward-looking</span>
                        </div>
                        <div className="flex justify-between items-start">
                          <span className="text-gray-700 font-medium">Rhetorical Style</span>
                          <span className="text-gray-600 text-right text-sm">evidence-based argumentation</span>
                        </div>
                      </div>
                    </div>

                    {/* Card 4: Fingerprint Summary */}
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
                            {`0x${Math.random().toString(16).substring(2, 50).padEnd(48, '0')}`}
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div className="bg-blue-50 rounded-lg p-4 text-center">
                            <div className="text-3xl font-bold text-blue-600 mb-1">96%</div>
                            <div className="text-sm text-gray-600">Uniqueness Score</div>
                          </div>
                          <div className="bg-green-50 rounded-lg p-4 text-center">
                            <div className="text-xl font-bold text-green-600 mb-1">Very High</div>
                            <div className="text-sm text-gray-600">Protection Level</div>
                          </div>
                        </div>

                        <div className="bg-purple-50 rounded-lg p-4 text-center">
                          <div className="text-xl font-bold text-purple-600 mb-1">High</div>
                          <div className="text-sm text-gray-600">Complexity Score</div>
                          <div className="text-xs text-gray-500 mt-1">(strategic policy document)</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Approve Button */}
                  {currentStep === 'preview' && (
                    <div className="flex justify-between items-center relative z-10">
                      <Link
                        href="/register/view-json"
                        className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                      >
                        View JSON
                      </Link>
                      <button
                        onClick={handleApproveFingerprint}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                      >
                        Approve Fingerprint
                      </button>
                    </div>
                  )}

                  {['approved', 'registered'].includes(currentStep) && (
                    <div className="flex justify-end relative z-10">
                      <div className="inline-flex items-center px-6 py-3 rounded-lg bg-green-100 text-green-700 font-medium">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Fingerprint Approved
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {/* Step 3: Register on Blockchain */}
          {['approved', 'registered'].includes(currentStep) && (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-10" style={{ backgroundImage: 'url(/blockchain.jpg)' }}></div>
              <div className="flex items-center gap-3 mb-6 relative z-10">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  currentStep === 'registered' ? 'bg-green-600' : 'bg-blue-600'
                }`}>
                  {currentStep === 'registered' ? (
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="text-white font-bold text-lg">3</span>
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Register on Blockchain</h2>
              </div>

              <div className="bg-gray-50/50 rounded-lg p-12 text-center relative z-10">
                <div className="flex justify-center mb-6">
                  <div className={`w-20 h-20 rounded-full flex items-center justify-center ${
                    registering ? 'bg-blue-200 animate-pulse' : currentStep === 'registered' ? 'bg-green-200' : 'bg-gray-200'
                  }`}>
                    <img 
                      src="/symbol-dark.png" 
                      alt="Story Protocol" 
                      className="w-12 h-12 object-contain"
                    />
                  </div>
                </div>

                <h3 className="text-2xl font-bold text-gray-700 mb-2">
                  {registering ? 'Registering on Story Protocol...' : currentStep === 'registered' ? 'Successfully Registered!' : 'Register IP Asset on Story Protocol'}
                </h3>
                <p className="text-gray-600 mb-8">
                  {registering ? 'Processing blockchain transaction...' : currentStep === 'registered' ? 'Your content is now protected on the blockchain' : 'Secure your content with immutable blockchain protection'}
                </p>

                {currentStep === 'approved' && (
                  <>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                      <div className="bg-white/60 rounded-lg border border-gray-200 p-6">
                        <div className="flex justify-center mb-3">
                          <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                          </svg>
                        </div>
                        <h4 className="font-bold text-gray-700 mb-1">Immutable Protection</h4>
                      </div>

                      <div className="bg-white/60 rounded-lg border border-gray-200 p-6">
                        <div className="flex justify-center mb-3">
                          <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <h4 className="font-bold text-gray-700 mb-1">Global Recognition</h4>
                      </div>

                      <div className="bg-white/60 rounded-lg border border-gray-200 p-6">
                        <div className="flex justify-center mb-3">
                          <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                          </svg>
                        </div>
                        <h4 className="font-bold text-gray-700 mb-1">Proof of Ownership</h4>
                      </div>
                    </div>

                    <button
                      onClick={handleRegister}
                      disabled={registering}
                      className={`px-8 py-3 rounded-lg font-medium flex items-center gap-2 mx-auto transition-colors ${
                        registering
                          ? 'bg-blue-400 text-white cursor-wait'
                          : 'bg-blue-600 hover:bg-blue-700 text-white'
                      }`}
                    >
                      {registering ? (
                        <>
                          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Processing Transaction...
                        </>
                      ) : (
                        <>
                          <img 
                            src="/symbol-dark.png" 
                            alt="Story Protocol" 
                            className="w-5 h-5 object-contain"
                          />
                          Register IP Asset
                        </>
                      )}
                    </button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Registration Progress */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Registration Progress</h2>

            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-900 font-medium">
                {currentStep === 'registered' ? 'Complete!' : `Step ${
                  currentStep === 'upload' || currentStep === 'analyze' ? '1' :
                  currentStep === 'build' || currentStep === 'preview' || currentStep === 'approved' ? '2' : '3'
                } in progress`}
              </span>
              <div className="flex items-center gap-6">
                <span className="text-gray-900 font-bold">
                  {Math.round(progressPercentage)}%
                </span>
                <div className="text-right">
                  <div className="font-bold text-gray-900">
                    {currentStep === 'registered' ? 'Complete!' : registering ? 'Processing...' : 'In Progress'}
                  </div>
                  <div className="text-sm text-gray-600">
                    {currentStep === 'registered' 
                      ? 'IP asset registered successfully'
                      : registering
                      ? 'Please wait...'
                      : 'Follow the steps above'
                    }
                  </div>
                </div>
              </div>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${currentStep === 'registered' ? 'bg-green-600' : 'bg-blue-600'}`}
                style={{width: `${progressPercentage}%`}}
              ></div>
            </div>
          </div>

          {/* Success Card - Shows after registration */}
          {currentStep === 'registered' && result && (
            <div className="bg-white rounded-lg border-2 border-green-500 p-6 mb-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">Successfully Registered!</h3>
                    <p className="text-gray-600">Your IP is now protected on the blockchain</p>
                  </div>
                </div>
                {result.source === 'blockchain' ? (
                  <span className="inline-flex items-center px-4 py-2 rounded-lg bg-green-100 border border-green-500 text-green-700 text-sm font-semibold">
                    ✅ Live Blockchain
                  </span>
                ) : (
                  <span className="inline-flex items-center px-4 py-2 rounded-lg bg-yellow-100 border border-yellow-500 text-yellow-700 text-sm font-semibold">
                    ⚠️ Mock Mode (Demo)
                  </span>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm font-semibold text-gray-700 mb-2">IP Asset ID</div>
                  <div className="font-mono text-xs text-gray-900 break-all mb-2">{result.ipAssetId}</div>
                  {result.source === 'blockchain' && (
                    <a
                      href={getIPAssetUrl(result.ipAssetId)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 text-xs font-medium"
                    >
                      View IP Asset →
                    </a>
                  )}
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm font-semibold text-gray-700 mb-2">IPFS Hash</div>
                  <div className="font-mono text-xs text-gray-900 break-all mb-2">{result.ipfsHash}</div>
                  {result.source === 'blockchain' && (
                    <a
                      href={getIPFSUrl(result.ipfsHash)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 text-xs font-medium"
                    >
                      View on IPFS →
                    </a>
                  )}
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm font-semibold text-gray-700 mb-2">Transaction Hash</div>
                  <div className="font-mono text-xs text-gray-900 break-all mb-2">{result.txHash}</div>
                  {result.source === 'blockchain' && (
                    <a
                      href={getExplorerUrl(result.txHash)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 text-xs font-medium"
                    >
                      View on Explorer →
                    </a>
                  )}
                </div>

                {result.tokenId && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm font-semibold text-gray-700 mb-2">Token ID</div>
                    <div className="font-mono text-xs text-gray-900 break-all">{result.tokenId}</div>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-center">
                <Link
                  href="/"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors inline-flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  Return to Dashboard
                </Link>
              </div>
            </div>
          )}
          </div>
        </main>
      </div>
    </div>
  );
}
