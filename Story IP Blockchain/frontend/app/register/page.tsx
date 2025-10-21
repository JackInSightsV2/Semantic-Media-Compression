'use client';

import { useState } from 'react';
import Link from 'next/link';
import SemanticDisplay from '@/components/SemanticDisplay';

// Import mock data
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
  
  async function handleRegister() {
    setRegistering(true);
    
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    setResult({
      ipAssetId: '0x' + Math.random().toString(16).substr(2, 40),
      ipfsHash: 'Qm' + Math.random().toString(36).substr(2, 44),
      txHash: '0x' + Math.random().toString(16).substr(2, 64),
    });
    
    setRegistered(true);
    setRegistering(false);
  }
  
  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl" />
      </div>
      
      {/* Navbar */}
      <nav className="relative glass-card border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center">
          <Link href="/" className="flex items-center text-purple-400 hover:text-purple-300 transition-colors mr-6">
            <span className="text-xl mr-2">←</span>
            <span className="font-semibold">Back</span>
          </Link>
          <h1 className="text-2xl font-bold text-white">
            Register Semantic IP
          </h1>
        </div>
      </nav>
      
      <main className="relative max-w-5xl mx-auto px-6 py-12">
        {/* Step 1 */}
        <div className="mb-10">
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-purple-500 rounded-xl flex items-center justify-center font-bold text-white mr-4">
              1
            </div>
            <h2 className="text-2xl font-semibold text-white">
              Select Content
            </h2>
          </div>
          <select 
            value={selected}
            onChange={(e) => setSelected(e.target.value as keyof typeof demoContent)}
            className="input-field text-white"
            disabled={registering || registered}
          >
            <option value="original-1">Demo Content 1: The Crossroads Decision</option>
            <option value="original-2">Demo Content 2: Rising Above</option>
            <option value="original-3">Demo Content 3: Behind the Facade</option>
          </select>
        </div>
        
        {/* Step 2 */}
        <div className="mb-10">
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-purple-500 rounded-xl flex items-center justify-center font-bold text-white mr-4">
              2
            </div>
            <h2 className="text-2xl font-semibold text-white">
              Preview Semantic Fingerprint
            </h2>
          </div>
          
          {/* Content Preview */}
          <div className="glass-card p-8 mb-6">
            <div className="relative h-80 bg-gradient-to-br from-purple-900/20 to-blue-900/20 rounded-2xl flex flex-col items-center justify-center mb-6 overflow-hidden">
              <div className="absolute inset-0 shimmer" />
              <div className="relative text-6xl mb-4">🎬</div>
              <div className="relative text-white/80 text-xl font-semibold">{currentData.metadata.title}</div>
            </div>
            <p className="text-gray-400 text-center leading-relaxed">
              {currentData.metadata.description}
            </p>
          </div>
          
          {/* Semantic Layers */}
          <SemanticDisplay data={currentData} />
        </div>
        
        {/* Step 3 */}
        <div className="mb-10">
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-purple-500 rounded-xl flex items-center justify-center font-bold text-white mr-4">
              3
            </div>
            <h2 className="text-2xl font-semibold text-white">
              Register on Blockchain
            </h2>
          </div>
          
          <button 
            onClick={handleRegister}
            disabled={registering || registered}
            className="btn-primary w-full text-lg"
          >
            {registering ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-6 w-6 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Processing Transaction...
              </span>
            ) : registered ? (
              '✅ Successfully Registered!'
            ) : (
              '🛡️ Register IP Asset on Story Protocol'
            )}
          </button>
        </div>
        
        {/* Loading State */}
        {registering && (
          <div className="glass-card p-12 text-center border-2 border-purple-500/30">
            <div className="inline-block mb-6">
              <div className="w-20 h-20 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-4">
              Processing Blockchain Transaction
            </h3>
            <p className="text-gray-400">
              Uploading semantic fingerprint to IPFS and registering on Story Protocol
            </p>
            <div className="mt-6 flex items-center justify-center gap-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" />
              <span>This may take a few moments...</span>
            </div>
          </div>
        )}
        
        {/* Success State */}
        {registered && result && (
          <div className="glass-card p-10 border-2 border-green-500/30 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-green-600/5 to-transparent" />
            <div className="relative">
              <div className="flex items-center mb-8">
                <div className="text-6xl mr-4">✅</div>
                <div>
                  <h3 className="text-3xl font-bold text-white mb-2">
                    Successfully Registered!
                  </h3>
                  <p className="text-gray-400">Your IP is now protected on the blockchain</p>
                </div>
              </div>
              
              <div className="space-y-6">
                <div>
                  <div className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-2">IP Asset ID</div>
                  <div className="glass-card p-4 font-mono text-sm text-white break-all">
                    {result.ipAssetId}
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-2">IPFS Hash</div>
                  <div className="glass-card p-4 font-mono text-sm text-white break-all">
                    {result.ipfsHash}
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-2">Transaction Hash</div>
                  <div className="glass-card p-4 font-mono text-sm text-white break-all">
                    {result.txHash}
                  </div>
                </div>
                <div className="pt-4">
                  <a 
                    href="#" 
                    className="inline-flex items-center text-purple-400 hover:text-purple-300 font-semibold transition-colors"
                    onClick={(e) => e.preventDefault()}
                  >
                    View on Story Protocol Explorer 
                    <span className="ml-2">→</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
