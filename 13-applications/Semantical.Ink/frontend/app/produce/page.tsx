
'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import { FaMagic, FaArrowRight, FaRobot, FaPalette, FaStore, FaLayerGroup, FaTimes, FaCheck, FaSearch, FaBook, FaFilm, FaHeadphones, FaCodeBranch, FaCoins } from 'react-icons/fa';
import { mockMarketplaceListings, mockAssets, Asset, MarketplaceListing } from '@/app/data/mockData';
import Link from 'next/link';

export default function ProducePage() {
  const [step, setStep] = useState(1);
  const [sourceType, setSourceType] = useState<'marketplace' | 'library' | null>(null);
  const [showSourceModal, setShowSourceModal] = useState(false);
  const [selectedSource, setSelectedSource] = useState<Asset | MarketplaceListing | null>(null);
  const [transformationType, setTransformationType] = useState<'format' | 'style' | null>(null);
  const [targetFormat, setTargetFormat] = useState<string>('');
  const [stylePrompt, setStylePrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedAsset, setGeneratedAsset] = useState<Asset | null>(null);
  const [assetTitle, setAssetTitle] = useState('');
  const [assetDescription, setAssetDescription] = useState('');

  // Filtered lists for modals
  const [searchTerm, setSearchTerm] = useState('');

  const getFilteredItems = () => {
    if (sourceType === 'marketplace') {
      return mockMarketplaceListings.filter(item =>
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.tags?.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    } else {
      return mockAssets.filter(item =>
        item.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
  };

  const handleSourceTypeSelect = (type: 'marketplace' | 'library') => {
    setSourceType(type);
    setShowSourceModal(true);
    setSearchTerm('');
  };

  const handleSourceSelect = (item: Asset | MarketplaceListing) => {
    setSelectedSource(item);
    setShowSourceModal(false);
    setStep(2);
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate API call
    setTimeout(() => {
      setIsGenerating(false);
      const newTitle = `Remix of ${selectedSource?.title}`;
      const newDescription = transformationType === 'style'
        ? `Style adaptation: ${stylePrompt}`
        : `A ${transformationType} transformation of ${selectedSource?.title}.`;

      setAssetTitle(newTitle);
      setAssetDescription(newDescription);

      setGeneratedAsset({
        id: 'new_generated_id',
        title: newTitle,
        type: 'derivative',
        format: targetFormat as any || 'script',
        status: 'processing',
        thumbnailUrl: selectedSource?.thumbnailUrl || '',
        createdAt: new Date().toISOString(),
        description: newDescription,
        author: 'You'
      });
    }, 3000);
  };

  const getIcon = (format: string) => {
    switch (format) {
      case 'novel': return <FaBook />;
      case 'script': return <FaFilm />;
      case 'audio': return <FaHeadphones />;
      case 'comic': return <FaPalette />;
      default: return <FaBook />;
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto relative">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-black text-slate-900 mb-4">
            Create <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-pink to-brand-purple">Derivative</span>
          </h1>
          <p className="text-xl text-slate-500">
            Transform existing IP into new formats using Semantic AI.
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex justify-center mb-12">
          <div className="flex items-center gap-4">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg transition-colors ${step >= s ? 'bg-brand-pink text-white' : 'bg-slate-200 text-slate-400'
                  }`}>
                  {s}
                </div>
                {s < 3 && <div className={`w-16 h-1 bg-slate-200 ${step > s ? 'bg-brand-pink' : ''}`} />}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-xl min-h-[400px]">
          {step === 1 && (
            <div className="text-center py-10">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Select Source Material</h2>
              <p className="text-slate-500 mb-8 max-w-md mx-auto">
                Choose a blueprint to start the transformation process.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
                {/* Marketplace Option */}
                <button
                  onClick={() => handleSourceTypeSelect('marketplace')}
                  className="group relative p-8 bg-white border border-slate-200 rounded-3xl hover:border-brand-pink hover:shadow-xl transition-all text-left flex flex-col items-center text-center"
                >
                  <div className="w-20 h-20 bg-brand-pink/10 rounded-full flex items-center justify-center mb-6 text-brand-pink group-hover:scale-110 transition-transform">
                    <FaStore size={32} />
                  </div>
                  <h3 className="text-xl font-black text-slate-900 mb-2">Choose from Marketplace</h3>
                  <p className="text-slate-500 text-sm">
                    Remix existing blueprints from top creators.
                  </p>
                  <div className="mt-6 px-6 py-2 bg-slate-50 text-slate-600 font-bold rounded-full group-hover:bg-brand-pink group-hover:text-white transition-colors">
                    Browse Gallery
                  </div>
                </button>

                {/* Library Option */}
                <button
                  onClick={() => handleSourceTypeSelect('library')}
                  className="group relative p-8 bg-white border border-slate-200 rounded-3xl hover:border-brand-cyan hover:shadow-xl transition-all text-left flex flex-col items-center text-center"
                >
                  <div className="w-20 h-20 bg-brand-cyan/10 rounded-full flex items-center justify-center mb-6 text-brand-cyan group-hover:scale-110 transition-transform">
                    <FaLayerGroup size={32} />
                  </div>
                  <h3 className="text-xl font-black text-slate-900 mb-2">Choose from My Own</h3>
                  <p className="text-slate-500 text-sm">
                    Use your own registered IP from your library.
                  </p>
                  <div className="mt-6 px-6 py-2 bg-slate-50 text-slate-600 font-bold rounded-full group-hover:bg-brand-cyan group-hover:text-white transition-colors">
                    Select from Library
                  </div>
                </button>
              </div>
            </div>
          )}

          {step === 2 && selectedSource && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-slate-900">Configure Transformation</h2>
                <button onClick={() => setStep(1)} className="text-sm text-slate-500 hover:text-brand-pink font-bold">
                  Change Source
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Selected Source Card */}
                <div className="lg:col-span-1">
                  <div className="bg-slate-50 rounded-2xl p-4 border border-slate-200">
                    <div className="aspect-video rounded-xl overflow-hidden mb-4 relative">
                      <img src={selectedSource.thumbnailUrl} alt={selectedSource.title} className="w-full h-full object-cover" />
                      <div className="absolute top-2 right-2 bg-black/50 backdrop-blur-md text-white text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
                        {getIcon(selectedSource.format)} {selectedSource.format}
                      </div>
                    </div>
                    <h3 className="font-bold text-slate-900 mb-1">{selectedSource.title}</h3>
                    <p className="text-xs text-slate-500 mb-3">By {selectedSource.author}</p>
                    <div className="flex flex-wrap gap-1">
                      {selectedSource.tags?.slice(0, 3).map(tag => (
                        <span key={tag} className="text-[10px] bg-white border border-slate-200 px-2 py-1 rounded-full text-slate-500 font-bold">#{tag}</span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Configuration Options */}
                <div className="lg:col-span-2 space-y-6">
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-3">Transformation Type</label>
                    <div className="grid grid-cols-2 gap-4">
                      <button
                        onClick={() => setTransformationType('format')}
                        className={`p-4 border-2 rounded-xl text-left transition-all ${transformationType === 'format' ? 'border-brand-pink bg-brand-pink/5' : 'border-slate-100 hover:border-slate-300'}`}
                      >
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 ${transformationType === 'format' ? 'bg-brand-pink text-white' : 'bg-slate-100 text-slate-400'}`}>
                          <FaRobot />
                        </div>
                        <div className="font-bold text-slate-900">Format Shift</div>
                        <div className="text-xs text-slate-500">Convert to a different medium</div>
                      </button>

                      <button
                        onClick={() => setTransformationType('style')}
                        className={`p-4 border-2 rounded-xl text-left transition-all ${transformationType === 'style' ? 'border-brand-cyan bg-brand-cyan/5' : 'border-slate-100 hover:border-slate-300'}`}
                      >
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 ${transformationType === 'style' ? 'bg-brand-cyan text-white' : 'bg-slate-100 text-slate-400'}`}>
                          <FaPalette />
                        </div>
                        <div className="font-bold text-slate-900">Style Adaptation</div>
                        <div className="text-xs text-slate-500">Rewrite in a new style</div>
                      </button>
                    </div>
                  </div>

                  {transformationType === 'format' && (
                    <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                      <label className="block text-sm font-bold text-slate-700 mb-3">Target Format</label>
                      <div className="flex flex-wrap gap-3">
                        {['novel', 'script', 'comic', 'audio', 'game'].filter(f => f !== selectedSource.format).map(fmt => (
                          <button
                            key={fmt}
                            onClick={() => setTargetFormat(fmt)}
                            className={`px-4 py-2 rounded-full border-2 font-bold text-sm capitalize transition-all ${targetFormat === fmt ? 'border-brand-purple bg-brand-purple text-white' : 'border-slate-200 text-slate-500 hover:border-brand-purple/50'}`}
                          >
                            {fmt}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {transformationType === 'style' && (
                    <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                      <label className="block text-sm font-bold text-slate-700 mb-3">Describe Target Style</label>
                      <textarea
                        value={stylePrompt}
                        onChange={(e) => setStylePrompt(e.target.value)}
                        placeholder="E.g., In the style of H.P. Lovecraft, Cyberpunk noir, Wes Anderson aesthetic..."
                        className="w-full p-4 rounded-xl border-2 border-slate-200 focus:border-brand-cyan focus:ring-0 transition-all font-medium text-slate-700 placeholder:text-slate-400 min-h-[120px]"
                      />
                    </div>
                  )}

                  <div className="pt-6 flex justify-end">
                    <button
                      onClick={() => setStep(3)}
                      disabled={!transformationType || (transformationType === 'format' && !targetFormat) || (transformationType === 'style' && !stylePrompt)}
                      className="px-8 py-3 bg-brand-pink text-white font-bold rounded-full hover:bg-brand-pink/90 transition-colors inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next Step <FaArrowRight />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="text-center py-10">
              {!isGenerating && !generatedAsset ? (
                <div className="animate-in fade-in zoom-in duration-300">
                  <div className="w-24 h-24 bg-brand-yellow/10 rounded-full flex items-center justify-center mx-auto mb-6 text-brand-yellow animate-pulse">
                    <FaMagic size={40} />
                  </div>
                  <h2 className="text-3xl font-black text-slate-900 mb-4">Ready to Generate</h2>
                  <p className="text-slate-500 mb-8 max-w-md mx-auto">
                    Transforming <strong>{selectedSource?.title}</strong> into a <strong>{targetFormat || 'new style'}</strong>.
                    <br />This will consume <span className="font-bold text-brand-pink">5 Credits</span>. The result will be generated as a draft for your review.
                  </p>

                  <button
                    onClick={handleGenerate}
                    className="px-10 py-4 bg-gradient-to-r from-brand-pink to-brand-purple text-white font-black text-lg rounded-full shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
                  >
                    Generate Derivative
                  </button>

                  <button onClick={() => setStep(2)} className="block mx-auto mt-6 text-slate-400 font-bold hover:text-slate-600">
                    Go Back
                  </button>
                </div>
              ) : isGenerating ? (
                <div className="py-20">
                  <div className="w-20 h-20 border-4 border-brand-pink border-t-transparent rounded-full animate-spin mx-auto mb-8"></div>
                  <h2 className="text-2xl font-bold text-slate-900 animate-pulse">Generating Assets...</h2>
                  <p className="text-slate-400 mt-2">Analyzing semantic structure...</p>
                </div>
              ) : (
                <div className="animate-in fade-in zoom-in duration-500">
                  <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 text-green-500">
                    <FaCheck size={32} />
                  </div>
                  <h2 className="text-3xl font-black text-slate-900 mb-2">Generation Complete!</h2>
                  <p className="text-slate-500 mb-8">Review your new asset before registering it on the blockchain.</p>

                  <div className="max-w-md mx-auto bg-slate-50 rounded-2xl p-4 border border-slate-200 mb-8 text-left flex gap-4">
                    <div className="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0 bg-slate-200">
                      <img src={generatedAsset?.thumbnailUrl} className="w-full h-full object-cover" />
                    </div>
                    <div className="flex-1">
                      <div className="mb-2">
                        <label className="block text-xs font-bold text-slate-500 mb-1">Title</label>
                        <input
                          type="text"
                          value={assetTitle}
                          onChange={(e) => {
                            setAssetTitle(e.target.value);
                            if (generatedAsset) setGeneratedAsset({ ...generatedAsset, title: e.target.value });
                          }}
                          className="w-full px-2 py-1 text-sm font-bold text-slate-900 bg-white border border-slate-200 rounded focus:border-brand-pink focus:outline-none"
                        />
                      </div>
                      <div className="mb-2">
                        <label className="block text-xs font-bold text-slate-500 mb-1">Description</label>
                        <textarea
                          value={assetDescription}
                          onChange={(e) => {
                            setAssetDescription(e.target.value);
                            if (generatedAsset) setGeneratedAsset({ ...generatedAsset, description: e.target.value });
                          }}
                          className="w-full px-2 py-1 text-xs text-slate-500 bg-white border border-slate-200 rounded focus:border-brand-pink focus:outline-none resize-none"
                          rows={2}
                        />
                      </div>
                      <div className="mt-2 text-xs font-bold text-brand-purple bg-brand-purple/10 px-2 py-1 rounded-full inline-block">
                        {generatedAsset?.format}
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-center gap-4">
                    <Link href="/library" className="px-6 py-3 bg-slate-100 text-slate-700 font-bold rounded-full hover:bg-slate-200 transition-colors">
                      Save as Draft
                    </Link>
                    <Link href="/marketplace" className="px-6 py-3 bg-brand-pink text-white font-bold rounded-full hover:bg-brand-pink/90 transition-colors">
                      Register & List
                    </Link>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Source Selection Modal */}
        {showSourceModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
            <div className="bg-white rounded-3xl w-full max-w-4xl max-h-[80vh] flex flex-col shadow-2xl">
              <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                <h3 className="text-2xl font-bold text-slate-900">
                  Select from {sourceType === 'marketplace' ? 'Marketplace' : 'Library'}
                </h3>
                <button onClick={() => setShowSourceModal(false)} className="p-2 hover:bg-slate-100 rounded-full text-slate-400 hover:text-slate-600 transition-colors">
                  <FaTimes size={20} />
                </button>
              </div>

              <div className="p-6 border-b border-slate-100 bg-slate-50">
                <div className="relative">
                  <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search assets..."
                    className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:border-brand-pink focus:ring-2 focus:ring-brand-pink/20 transition-all"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {getFilteredItems().map((item) => (
                    <button
                      key={item.id}
                      onClick={() => handleSourceSelect(item)}
                      className="group bg-white border border-slate-200 rounded-2xl overflow-hidden hover:border-brand-pink hover:shadow-lg transition-all text-left flex flex-col h-full"
                    >
                      <div className="h-40 overflow-hidden relative">
                        <img src={item.thumbnailUrl} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                        <div className="absolute top-2 right-2 bg-black/50 backdrop-blur-md text-white text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
                          {getIcon(item.format)} {item.format}
                        </div>
                      </div>
                      <div className="p-4 flex-1 flex flex-col">
                        <h4 className="font-bold text-slate-900 mb-1 line-clamp-1">{item.title}</h4>
                        <p className="text-xs text-slate-500 mb-3">By {item.author}</p>
                        <div className="mt-auto flex items-center justify-between">
                          {'priceCredits' in item ? (
                            <div className="flex items-center gap-1 text-sm font-bold text-brand-dark">
                              <FaCoins className="text-brand-yellow" /> {(item as MarketplaceListing).priceCredits}
                            </div>
                          ) : (
                            <div className="text-xs font-bold text-green-500 bg-green-50 px-2 py-1 rounded-full">
                              Owned
                            </div>
                          )}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
                {getFilteredItems().length === 0 && (
                  <div className="text-center py-20 text-slate-400">
                    No items found matching "{searchTerm}"
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
