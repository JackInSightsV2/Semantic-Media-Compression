'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function DisputePage() {
  const [originalIP, setOriginalIP] = useState('');
  const [suspectedIP, setSuspectedIP] = useState('');
  const [filing, setFiling] = useState(false);
  const [filed, setFiled] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  // Mock registered IPs
  const mockIPs = [
    { id: '0x1234...abcd', title: 'The Crossroads Decision', similarity: '91%' },
    { id: '0x5678...efgh', title: 'Rising Above', similarity: '89%' },
    { id: '0x9abc...ijkl', title: 'Behind the Facade', similarity: '93%' },
  ];
  
  async function handleFileDispute() {
    if (!originalIP || !suspectedIP) return;
    
    setFiling(true);
    
    // Simulate blockchain transaction
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Mock result
    setResult({
      disputeId: '0xdisp' + Math.random().toString(16).substr(2, 36),
      evidenceIPFS: 'Qmevidence' + Math.random().toString(36).substr(2, 38),
      txHash: '0x' + Math.random().toString(16).substr(2, 64),
    });
    
    setFiled(true);
    setFiling(false);
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
            File Plagiarism Dispute
          </h1>
        </div>
      </nav>
      
      <main className="max-w-4xl mx-auto px-4 pb-12">
        {/* Step 1: Select IP Assets */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-6 text-gray-900">
            Step 1: Select IP Assets
          </h2>
          
          <div className="bg-white rounded-lg p-6 shadow-md space-y-6">
            <div>
              <label className="block font-semibold text-gray-700 mb-2">
                Original IP Asset:
              </label>
              <select 
                value={originalIP}
                onChange={(e) => setOriginalIP(e.target.value)}
                className="select"
                disabled={filing || filed}
              >
                <option value="">Select your registered IP...</option>
                <option value="0x1234...abcd">0x1234...abcd - The Crossroads Decision</option>
                <option value="0x5678...efgh">0x5678...efgh - Rising Above</option>
                <option value="0x9abc...ijkl">0x9abc...ijkl - Behind the Facade</option>
              </select>
            </div>
            
            <div>
              <label className="block font-semibold text-gray-700 mb-2">
                Suspected Plagiarism IP Asset:
              </label>
              <select 
                value={suspectedIP}
                onChange={(e) => setSuspectedIP(e.target.value)}
                className="select"
                disabled={filing || filed}
              >
                <option value="">Select suspected copycat...</option>
                <option value="0xaabb...ccdd">0xaabb...ccdd - The Difficult Path (91% similar)</option>
                <option value="0xeeff...gghh">0xeeff...gghh - Ascending Heights (89% similar)</option>
                <option value="0xiijj...kkll">0xiijj...kkll - Unmasking Secrets (93% similar)</option>
              </select>
            </div>
          </div>
        </div>
        
        {/* Step 2: Evidence Package */}
        {originalIP && suspectedIP && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-6 text-gray-900">
              Step 2: Review Evidence Package
            </h2>
            
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-bold text-red-700 mb-4">
                  Evidence Summary
                </h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="font-semibold">Overall Similarity:</span>
                    <span className="text-red-600 font-bold">91%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-semibold">Plagiarism Confidence:</span>
                    <span className="text-red-600 font-bold">HIGH</span>
                  </div>
                  
                  <hr className="border-red-200" />
                  
                  <div>
                    <p className="font-semibold mb-2">Dimensional Analysis:</p>
                    <ul className="space-y-1 ml-4">
                      <li>• Narrative Structure: <span className="text-red-600 font-semibold">94% match</span></li>
                      <li>• Character Essence: <span className="text-red-600 font-semibold">89% match</span></li>
                      <li>• Thematic Content: <span className="text-red-600 font-semibold">88% match</span></li>
                    </ul>
                  </div>
                  
                  <hr className="border-red-200" />
                  
                  <div>
                    <p className="font-semibold mb-2">Matching Elements:</p>
                    <ul className="space-y-1 ml-4">
                      <li>• Identical narrative arc structure</li>
                      <li>• Same character archetype and development</li>
                      <li>• Matching primary and secondary themes</li>
                      <li>• Similar emotional progression pattern</li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                <p className="flex items-start">
                  <span className="text-xl mr-2">ℹ️</span>
                  <span>
                    This evidence package will be stored on IPFS and permanently linked 
                    to your dispute on the Story Protocol blockchain.
                  </span>
                </p>
              </div>
            </div>
          </div>
        )}
        
        {/* Submit Button */}
        <div className="mb-8">
          <button 
            onClick={handleFileDispute}
            disabled={!originalIP || !suspectedIP || filing || filed}
            className="btn-primary w-full md:w-auto px-12 py-4 text-lg"
          >
            {filing ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Filing Dispute...
              </span>
            ) : filed ? (
              '✓ Dispute Filed!'
            ) : (
              'Submit Dispute to Story Protocol'
            )}
          </button>
        </div>
        
        {/* Loading State */}
        {filing && (
          <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-8 text-center">
            <div className="inline-block animate-pulse mb-4">
              <div className="text-5xl">⚖️</div>
            </div>
            <p className="text-lg font-semibold text-purple-700">
              Processing blockchain transaction...
            </p>
            <p className="text-sm text-gray-600 mt-2">
              Uploading evidence to IPFS and filing dispute on Story Protocol
            </p>
          </div>
        )}
        
        {/* Success State */}
        {filed && result && (
          <div className="bg-green-50 border-2 border-green-500 rounded-lg p-8">
            <h3 className="text-2xl font-bold text-green-700 mb-6 flex items-center">
              <span className="text-4xl mr-3">✅</span>
              Dispute Filed Successfully!
            </h3>
            <div className="space-y-4">
              <div>
                <span className="font-semibold text-gray-700">Dispute ID:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.disputeId}
                </p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Evidence IPFS Hash:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.evidenceIPFS}
                </p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Transaction Hash:</span>
                <p className="text-sm font-mono bg-white p-2 rounded mt-1 break-all">
                  {result.txHash}
                </p>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Status:</span>
                <p className="mt-1">
                  <span className="inline-block px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold">
                    Pending Review
                  </span>
                </p>
              </div>
              <div className="pt-4">
                <a 
                  href="#" 
                  className="text-purple-600 hover:text-purple-700 font-semibold flex items-center"
                  onClick={(e) => e.preventDefault()}
                >
                  View Dispute on Story Protocol Explorer →
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

