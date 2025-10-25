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
 * @fingerprint SH:JI2:c1e4f7b0d3a6c9e2f5a8b1d4e7c0f3a6
 */

'use client';

import { useState } from 'react';
import Link from 'next/link';
import SemanticDisplay from '@/components/SemanticDisplay';
import SimilarityScore from '@/components/SimilarityScore';
import { fetchFromIPFS } from '@/blocklibs/ipfs';

// Import mock data
import situationalAwareness from '@/demo-data/situational_awareness.json';

// Get the first object from the array (main document overview)
const mainDocument = Array.isArray(situationalAwareness) ? situationalAwareness[0] : situationalAwareness;

// Transform the complex JSON structure to match SemanticDisplay's expected format
function transformToSemanticData(data: any): any {
  // Extract or generate a semantic fingerprint from the complex data structure
  const globalContext = data.global_context || {};
  const narrativeArc = globalContext.narrative_arc || {};
  const themes = globalContext.key_themes || [];
  
  return {
    ...data,
    content_id: data.document_metadata?.title || 'unknown',
    semantic_fingerprint: {
      narrative: {
        genre: data.document_metadata?.domain?.split(',')[0] || 'Strategic Essay',
        story_arc: narrativeArc.structure || 'Complex analytical progression',
        themes: Array.isArray(themes) ? themes.slice(0, 3) : ['AI capability forecasting', 'strategic analysis', 'future predictions'],
        dramatic_progression: Array.isArray(narrativeArc.dramatic_progression) 
          ? narrativeArc.dramatic_progression.join(' → ') 
          : 'Introduction to analysis to conclusions',
      },
      characters: {
        protagonist: {
          archetype: 'Analyst/Visionary',
          traits: ['analytical', 'strategic', 'forward-thinking'],
          arc: 'Presents evidence and builds toward recommendations',
        },
      },
      themes: {
        primary: globalContext.core_thesis || 'AI development and strategic implications',
        secondary: Array.isArray(globalContext.primary_objectives) 
          ? globalContext.primary_objectives.slice(0, 3)
          : ['Strategic planning', 'Risk assessment', 'Policy recommendations'],
        emotional_tone: 'Serious and analytical',
        visual_metaphors: ['scaling trends', 'capability thresholds', 'strategic competition'],
      },
    },
  };
}

// Use the same data for all demo content variations
const transformedDocument = transformToSemanticData(mainDocument);
const allContent = {
  'original-1': transformedDocument,
  'original-2': transformedDocument,
  'original-3': transformedDocument,
  'copycat-1': transformedDocument,
  'copycat-2': transformedDocument,
  'copycat-3': transformedDocument,
};

// Cosine similarity calculation
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magA * magB);
}

// Type for data with embeddings
type DataWithEmbeddings = any & {
  embeddings: {
    narrative_vector: number[];
    character_vector: number[];
    thematic_vector: number[];
  };
};

// Generate mock embeddings if they don't exist
function ensureEmbeddings(data: any): DataWithEmbeddings {
  if (data.embeddings) {
    return data as DataWithEmbeddings;
  }
  
  // Generate deterministic mock embeddings based on semantic fingerprint
  const narrative = data.semantic_fingerprint?.narrative || {};
  const characters = data.semantic_fingerprint?.characters || {};
  const themes = data.semantic_fingerprint?.themes || {};
  
  // Create 128-dimensional vectors with some variation
  const generateVector = (seed: string, dim: number = 128): number[] => {
    const vec = [];
    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
      hash = ((hash << 5) - hash) + seed.charCodeAt(i);
      hash = hash & hash;
    }
    
    for (let i = 0; i < dim; i++) {
      const val = Math.sin(hash + i * 0.1) * 0.5 + 0.5;
      vec.push(val);
    }
    
    // Normalize
    const mag = Math.sqrt(vec.reduce((sum, v) => sum + v * v, 0));
    return vec.map(v => v / mag);
  };
  
  return {
    ...data,
    embeddings: {
      narrative_vector: generateVector(JSON.stringify(narrative)),
      character_vector: generateVector(JSON.stringify(characters)),
      thematic_vector: generateVector(JSON.stringify(themes)),
    }
  } as DataWithEmbeddings;
}

export default function ComparePage() {
  const [original, setOriginal] = useState<keyof typeof allContent>('original-1');
  const [suspected, setSuspected] = useState<keyof typeof allContent>('copycat-1');
  const [comparing, setComparing] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [useIPFS, setUseIPFS] = useState(false);
  const [originalIPFSHash, setOriginalIPFSHash] = useState('');
  const [suspectedIPFSHash, setSuspectedIPFSHash] = useState('');
  const [ipfsError, setIpfsError] = useState('');
  
  const originalData = allContent[original];
  const suspectedData = allContent[suspected];
  
  async function handleCompare() {
    setComparing(true);
    setResults(null);
    setIpfsError('');
    
    try {
      let origData = originalData;
      let suspData = suspectedData;
      
      // Fetch from IPFS if enabled
      if (useIPFS) {
        try {
          if (!originalIPFSHash || !suspectedIPFSHash) {
            throw new Error('Please provide both IPFS hashes');
          }
          
          console.log('📥 Fetching from IPFS...');
          const [orig, susp] = await Promise.all([
            fetchFromIPFS(originalIPFSHash),
            fetchFromIPFS(suspectedIPFSHash)
          ]);
          
          origData = transformToSemanticData(orig);
          suspData = transformToSemanticData(susp);
          console.log('✅ Fetched from IPFS successfully');
        } catch (ipfsErr: any) {
          setIpfsError(`IPFS fetch failed: ${ipfsErr.message}. Using mock data instead.`);
          console.warn('⚠️ IPFS fetch failed, falling back to mock data');
          // Fall back to mock data
        }
      }
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Ensure embeddings exist (generate mock ones if needed)
      const origDataWithEmbeddings = ensureEmbeddings(origData);
      const suspDataWithEmbeddings = ensureEmbeddings(suspData);
      
      // Calculate actual similarity from embeddings
      const narrativeSim = cosineSimilarity(
        origDataWithEmbeddings.embeddings.narrative_vector,
        suspDataWithEmbeddings.embeddings.narrative_vector
      );
      const characterSim = cosineSimilarity(
        origDataWithEmbeddings.embeddings.character_vector,
        suspDataWithEmbeddings.embeddings.character_vector
      );
      const thematicSim = cosineSimilarity(
        origDataWithEmbeddings.embeddings.thematic_vector,
        suspDataWithEmbeddings.embeddings.thematic_vector
      );
      
      const overall = (narrativeSim * 0.4 + characterSim * 0.4 + thematicSim * 0.2);
      
      // Generate matching elements based on similarity
      const matchingElements = [];
      if (narrativeSim > 0.85) {
        matchingElements.push(`Identical narrative structure: ${origDataWithEmbeddings.semantic_fingerprint?.narrative?.story_arc || 'N/A'}`);
        matchingElements.push(`Matching genre: ${origDataWithEmbeddings.semantic_fingerprint?.narrative?.genre || 'N/A'}`);
      }
      if (characterSim > 0.85) {
        matchingElements.push(`Same character archetype: ${origDataWithEmbeddings.semantic_fingerprint?.characters?.protagonist?.archetype || 'N/A'}`);
      }
      if (thematicSim > 0.85) {
        matchingElements.push(`Matching primary theme: ${origDataWithEmbeddings.semantic_fingerprint?.themes?.primary || 'N/A'}`);
      }
      if (overall > 0.85) {
        matchingElements.push(`Similar emotional progression across all dimensions`);
      }
      
      setResults({
        overall,
        dimensions: {
          narrative: narrativeSim,
          character: characterSim,
          thematic: thematicSim,
        },
        level: overall > 0.85 ? 'HIGH' : overall > 0.70 ? 'MODERATE' : 'LOW',
        matching_elements: matchingElements,
      });
    } finally {
      setComparing(false);
    }
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
            Detect Semantic Plagiarism
          </h1>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto px-4 pb-12">
        {/* IPFS Mode Toggle */}
        <div className="mb-6 bg-white rounded-lg p-4 shadow-md">
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={useIPFS}
              onChange={(e) => setUseIPFS(e.target.checked)}
              className="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500"
            />
            <div>
              <span className="font-semibold text-gray-900">Fetch from IPFS</span>
              <p className="text-sm text-gray-600">Use registered content from IPFS instead of mock data</p>
            </div>
          </label>
          
          {useIPFS && (
            <div className="mt-4 grid md:grid-cols-2 gap-4 pt-4 border-t border-gray-200">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Original IPFS Hash</label>
                <input
                  type="text"
                  value={originalIPFSHash}
                  onChange={(e) => setOriginalIPFSHash(e.target.value)}
                  placeholder="Qm..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Suspected IPFS Hash</label>
                <input
                  type="text"
                  value={suspectedIPFSHash}
                  onChange={(e) => setSuspectedIPFSHash(e.target.value)}
                  placeholder="Qm..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>
            </div>
          )}
          
          {ipfsError && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">{ipfsError}</p>
            </div>
          )}
        </div>
        
        {/* Side-by-side comparison */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Original Content */}
          <div>
            <h2 className="text-xl font-semibold mb-4 text-purple-700">
              Original Content
            </h2>
            
            <div className="mb-4">
              <select 
                value={original}
                onChange={(e) => setOriginal(e.target.value as keyof typeof allContent)}
                className="select"
                disabled={comparing}
              >
                <option value="original-1">Original 1: The Crossroads Decision</option>
                <option value="original-2">Original 2: Rising Above</option>
                <option value="original-3">Original 3: Behind the Facade</option>
              </select>
            </div>
            
            {/* Image Preview */}
            <div className="bg-white rounded-lg p-4 mb-4 shadow-md">
              <div className="bg-gradient-to-r from-purple-200 to-purple-300 rounded-lg h-48 flex items-center justify-center">
                <span className="text-purple-700 text-sm">
                  [Original Image]
                </span>
              </div>
            </div>
            
            <SemanticDisplay data={originalData} compact />
          </div>
          
          {/* Suspected Plagiarism */}
          <div>
            <h2 className="text-xl font-semibold mb-4 text-red-700">
              Suspected Plagiarism
            </h2>
            
            <div className="mb-4">
              <select 
                value={suspected}
                onChange={(e) => setSuspected(e.target.value as keyof typeof allContent)}
                className="select"
                disabled={comparing}
              >
                <option value="copycat-1">Copycat 1: The Difficult Path</option>
                <option value="copycat-2">Copycat 2: Ascending Heights</option>
                <option value="copycat-3">Copycat 3: Unmasking Secrets</option>
              </select>
            </div>
            
            {/* Image Preview */}
            <div className="bg-white rounded-lg p-4 mb-4 shadow-md">
              <div className="bg-gradient-to-r from-red-200 to-red-300 rounded-lg h-48 flex items-center justify-center">
                <span className="text-red-700 text-sm">
                  [Suspected Image]
                </span>
              </div>
            </div>
            
            <SemanticDisplay data={suspectedData} compact />
          </div>
        </div>
        
        {/* Compare Button */}
        <div className="text-center mb-8">
          <button 
            onClick={handleCompare}
            disabled={comparing}
            className="btn-primary px-12 py-4 text-lg"
          >
            {comparing ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Analyzing Semantic Similarity...
              </span>
            ) : (
              'Compare Semantic Fingerprints'
            )}
          </button>
        </div>
        
        {/* Results */}
        {results && (
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <h2 className="text-3xl font-bold mb-8 text-center">
              Similarity Analysis Results
            </h2>
            <SimilarityScore results={results} />
            
            {/* Action Button */}
            {results.level === 'HIGH' && (
              <div className="mt-8 text-center">
                <Link 
                  href="/dispute"
                  className="inline-block bg-red-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-red-700 transition-colors"
                >
                  File Dispute on Story Protocol →
                </Link>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

