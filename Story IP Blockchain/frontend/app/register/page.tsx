'use client';

import { useState } from 'react';
import Link from 'next/link';
import SemanticDisplay from '@/components/SemanticDisplay';

// Import mock data (we'll load this from JSON files later)
import original1 from '@/../demo-data/original-1-semantic.json';
import original2 from '@/../demo-data/original-2-semantic.json';
import original3 from '@/../demo-data/original-3-semantic.json';

const demoContent = {
  'original-1': original1,
  'original-2': original2,
  'original-3': original3,
};

export default function RegisterPage() {
  const [selected, setSelected] = useState<keyof typeof demoContent>('original-1');
  const [registering, setRegistering] = useState(false);
  const [registered, setRegistered] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const currentData = demoContent[selected];
  
  // Mock registration process
  async function handleRegister() {
    setRegistering(true);
    
    // Simulate blockchain transaction
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Mock result
    setResult({
      ipAssetId: '0x' + Math.random().toString(16).substr(2, 40),
      ipfsHash: 'Qm' + Math.random().toString(36).substr(2, 44),
      txHash: '0x' + Math.random().toString(16).substr(2, 64),
    });
    
    setRegistered(true);
    setRegistering(false);
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center">
          <Link href="/" className="text-purple-600 hover:text-purple-700 mr-4">
            ← Back
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">
            Register Semantic IP
          </h1>
        </div>
      </nav>
      
      <main className="max-w-5xl mx-auto px-4 pb-12">
        {/* Step 1: Select Content */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">
            Step 1: Select Content
          </h2>
          <select 
            value={selected}
            onChange={(e) => setSelected(e.target.value as keyof typeof demoContent)}
            className="select"
            disabled={registering || registered}
          >
            <option value="original-1">Demo Content 1: The Crossroads Decision</option>
            <option value="original-2">Demo Content 2: Rising Above</option>
            <option value="original-3">Demo Content 3: Behind the Facade</option>
          </select>
        </div>
        
        {/* Step 2: Preview */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">
            Step 2: Preview Semantic Fingerprint
          </h2>
          
          {/* Image Preview */}
          <div className="bg-white rounded-lg p-6 mb-6 shadow-md">
            <div className="bg-gradient-to-r from-gray-200 to-gray-300 rounded-lg h-64 flex items-center justify-center mb-4">
              <span className="text-gray-500 text-lg">
                [Demo Image: {currentData.metadata.title}]
              </span>
            </div>
            <p className="text-gray-600 text-sm">
              {currentData.metadata.description}
            </p>
          </div>
          
          {/* Semantic Layers */}
          <SemanticDisplay data={currentData} />
        </div>
        
        {/* Step 3: Register Button */}
        <div className="mb-8">
          <button 
            onClick={handleRegister}
            disabled={registering || registered}
            className="btn-primary w-full md:w-auto"
          >
            {registering ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Registering on Story Protocol...
              </span>
            ) : registered ? (
              '✓ Successfully Registered!'
            ) : (
              'Register IP Asset on Story Protocol'
            )}
          </button>
        </div>
        
        {/* Loading State */}
        {registering && (
          <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-8 text-center">
            <div className="inline-block animate-pulse mb-4">
              <div className="text-5xl">⛓️</div>
            </div>
            <p className="text-lg font-semibold text-purple-700">
              Processing blockchain transaction...
            </p>
            <p className="text-sm text-gray-600 mt-2">
              Uploading semantic fingerprint to IPFS and registering on Story Protocol
            </p>
          </div>
        )}
        
        {/* Success State */}
        {registered && result && (
          <div className="bg-green-50 border-2 border-green-500 rounded-lg p-8">
            <h3 className="text-2xl font-bold text-green-700 mb-6 flex items-center">
              <span className="text-4xl mr-3">✅</span>
              Successfully Registered!
            </h3>
            <div className="space-y-4">
              <div>
                <span className="font-semibold text-gray-700">IP Asset ID:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.ipAssetId}
                </p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">IPFS Hash:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.ipfsHash}
                </p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Transaction Hash:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.txHash}
                </p>
              </div>
              <div className="pt-4">
                <a 
                  href="#" 
                  className="text-purple-600 hover:text-purple-700 font-semibold flex items-center"
                  onClick={(e) => e.preventDefault()}
                >
                  View on Story Protocol Explorer →
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

