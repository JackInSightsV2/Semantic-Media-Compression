'use client';

import { useState } from 'react';
import Link from 'next/link';
import SemanticDisplay from '@/components/SemanticDisplay';
import SimilarityScore from '@/components/SimilarityScore';

// Import mock data
import original1 from '@/../demo-data/original-1-semantic.json';
import original2 from '@/../demo-data/original-2-semantic.json';
import original3 from '@/../demo-data/original-3-semantic.json';
import copycat1 from '@/../demo-data/copycat-1-semantic.json';
import copycat2 from '@/../demo-data/copycat-2-semantic.json';
import copycat3 from '@/../demo-data/copycat-3-semantic.json';

const allContent = {
  'original-1': original1,
  'original-2': original2,
  'original-3': original3,
  'copycat-1': copycat1,
  'copycat-2': copycat2,
  'copycat-3': copycat3,
};

// Cosine similarity calculation
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magA * magB);
}

export default function ComparePage() {
  const [original, setOriginal] = useState<keyof typeof allContent>('original-1');
  const [suspected, setSuspected] = useState<keyof typeof allContent>('copycat-1');
  const [comparing, setComparing] = useState(false);
  const [results, setResults] = useState<any>(null);
  
  const originalData = allContent[original];
  const suspectedData = allContent[suspected];
  
  async function handleCompare() {
    setComparing(true);
    setResults(null);
    
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Calculate actual similarity from embeddings
    const narrativeSim = cosineSimilarity(
      originalData.embeddings.narrative_vector,
      suspectedData.embeddings.narrative_vector
    );
    const characterSim = cosineSimilarity(
      originalData.embeddings.character_vector,
      suspectedData.embeddings.character_vector
    );
    const thematicSim = cosineSimilarity(
      originalData.embeddings.thematic_vector,
      suspectedData.embeddings.thematic_vector
    );
    
    const overall = (narrativeSim * 0.4 + characterSim * 0.4 + thematicSim * 0.2);
    
    // Generate matching elements based on similarity
    const matchingElements = [];
    if (narrativeSim > 0.85) {
      matchingElements.push(`Identical narrative structure: ${originalData.semantic_fingerprint.narrative.story_arc}`);
      matchingElements.push(`Matching genre: ${originalData.semantic_fingerprint.narrative.genre}`);
    }
    if (characterSim > 0.85) {
      matchingElements.push(`Same character archetype: ${originalData.semantic_fingerprint.characters.protagonist.archetype}`);
    }
    if (thematicSim > 0.85) {
      matchingElements.push(`Matching primary theme: ${originalData.semantic_fingerprint.themes.primary}`);
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
    
    setComparing(false);
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

