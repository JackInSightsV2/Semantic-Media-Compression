
'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import { FaFingerprint, FaCheckCircle, FaExclamationTriangle, FaPlus, FaCloudUploadAlt, FaCode, FaFileContract, FaCoins, FaArrowRight, FaTimes } from 'react-icons/fa';
import Link from 'next/link';

export default function RegisterPage() {
    const [step, setStep] = useState(1);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisComplete, setAnalysisComplete] = useState(false);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    // Form State
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('10');
    const [licenseType, setLicenseType] = useState('commercial');
    const [royalty, setRoyalty] = useState('5');

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setUploadedFile(e.target.files[0]);
            setTitle(e.target.files[0].name.split('.')[0]); // Auto-fill title
        }
    };

    const handleAnalyze = () => {
        setIsAnalyzing(true);
        setTimeout(() => {
            setIsAnalyzing(false);
            setAnalysisComplete(true);
            setStep(2);
        }, 3000);
    };

    const handleRegister = () => {
        // Simulate registration
        setStep(4);
    };

    return (
        <DashboardLayout>
            <div className="max-w-4xl mx-auto">
                <div className="text-center py-10 relative">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-purple-500/20 blur-[100px] rounded-full pointer-events-none" />
                    <h1 className="text-5xl md:text-7xl font-black text-slate-900 mb-4 relative z-10">
                        Register <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-purple to-brand-pink">IP</span>
                    </h1>
                    <p className="text-xl text-slate-500 max-w-2xl mx-auto relative z-10">
                        Secure your creative assets on Story Protocol.
                    </p>
                </div>

                {/* Progress Steps */}
                {step < 4 && (
                    <div className="flex justify-center mb-12">
                        <div className="flex items-center gap-4">
                            {[1, 2, 3].map((s) => (
                                <div key={s} className="flex items-center gap-4">
                                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg transition-colors ${step >= s ? 'bg-brand-purple text-white' : 'bg-slate-200 text-slate-400'
                                        }`}>
                                        {s}
                                    </div>
                                    {s < 3 && <div className={`w-16 h-1 bg-slate-200 ${step > s ? 'bg-brand-purple' : ''}`} />}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-xl min-h-[400px]">

                    {/* Step 1: Upload & Analyze */}
                    {step === 1 && (
                        <div className="text-center py-10">
                            <h2 className="text-2xl font-bold text-slate-900 mb-4">Upload Source Material</h2>
                            <p className="text-slate-500 mb-8 max-w-md mx-auto">
                                Upload your novel, script, or audio file to begin the semantic analysis.
                            </p>

                            <div className="max-w-xl mx-auto mb-8">
                                <label className={`border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer transition-colors ${uploadedFile ? 'border-brand-purple bg-brand-purple/5' : 'border-slate-300 hover:border-brand-purple hover:bg-slate-50'}`}>
                                    <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf,.docx,.txt,.mp3,.wav" />
                                    {uploadedFile ? (
                                        <>
                                            <div className="w-16 h-16 bg-brand-purple/10 rounded-full flex items-center justify-center mb-4 text-brand-purple">
                                                <FaCheckCircle size={32} />
                                            </div>
                                            <div className="font-bold text-slate-900">{uploadedFile.name}</div>
                                            <div className="text-sm text-slate-500">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</div>
                                        </>
                                    ) : (
                                        <>
                                            <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4 text-slate-400">
                                                <FaCloudUploadAlt size={32} />
                                            </div>
                                            <div className="font-bold text-slate-900 mb-1">Click to Upload</div>
                                            <div className="text-sm text-slate-500">PDF, DOCX, TXT, MP3, WAV</div>
                                        </>
                                    )}
                                </label>
                            </div>

                            <button
                                onClick={handleAnalyze}
                                disabled={!uploadedFile || isAnalyzing}
                                className="px-8 py-3 bg-brand-purple text-white font-bold rounded-full hover:bg-brand-purple/90 transition-colors inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isAnalyzing ? (
                                    <>
                                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <FaCode /> Analyze Semantic Structure (5 Credits)
                                    </>
                                )}
                            </button>
                        </div>
                    )}

                    {/* Step 2: Review Analysis */}
                    {step === 2 && (
                        <div className="py-6">
                            <h2 className="text-2xl font-bold text-slate-900 mb-2 text-center">Analysis Complete</h2>
                            <p className="text-slate-500 mb-8 text-center">We've extracted the semantic structure of your asset.</p>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                                    <div className="text-xs font-bold text-slate-500 uppercase mb-1">Detected Genre</div>
                                    <div className="text-lg font-black text-slate-900">Sci-Fi Thriller</div>
                                </div>
                                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                                    <div className="text-xs font-bold text-slate-500 uppercase mb-1">Word Count</div>
                                    <div className="text-lg font-black text-slate-900">45,201</div>
                                </div>
                                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                                    <div className="text-xs font-bold text-slate-500 uppercase mb-1">Est. Reading Time</div>
                                    <div className="text-lg font-black text-slate-900">3h 12m</div>
                                </div>
                            </div>

                            <div className="mb-8">
                                <h3 className="text-sm font-bold text-slate-700 mb-3">Key Themes</h3>
                                <div className="flex flex-wrap gap-2">
                                    {['Redemption', 'Technology', 'Isolation', 'Artificial Intelligence', 'Survival'].map(theme => (
                                        <span key={theme} className="px-3 py-1 bg-brand-purple/10 text-brand-purple rounded-full text-sm font-bold">
                                            #{theme}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="bg-slate-900 rounded-xl p-6 font-mono text-sm text-green-400 overflow-x-auto mb-8 max-h-[300px] overflow-y-auto shadow-inner">
                                <div className="text-xs text-slate-500 mb-2 border-b border-slate-800 pb-2">RAW SEMANTIC DATA</div>
                                <pre>{`{
  "semantic_version": "1.0.0",
  "asset_type": "narrative_text",
  "structure": {
    "sentiment_arc": "positive_to_negative",
    "key_themes": ["redemption", "technology", "isolation"],
    "character_graph": {
      "nodes": 5,
      "edges": 12,
      "centrality": "protagonist_A"
    },
    "narrative_beats": [
      { "id": 1, "type": "inciting_incident", "confidence": 0.98 },
      { "id": 2, "type": "climax", "confidence": 0.95 }
    ]
  },
  "compatibility": {
    "format_shift": ["script", "comic", "audio_drama"],
    "style_transfer": ["high_fidelity"]
  }
}`}</pre>
                            </div>

                            <div className="flex justify-center gap-4">
                                <button onClick={() => setStep(1)} className="px-6 py-3 text-slate-500 font-bold hover:text-slate-700">
                                    Back
                                </button>
                                <button onClick={() => setStep(3)} className="px-8 py-3 bg-brand-purple text-white font-bold rounded-full hover:bg-brand-purple/90 transition-colors inline-flex items-center gap-2">
                                    Proceed to Registration <FaArrowRight />
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 3: Registration Details */}
                    {step === 3 && (
                        <div className="py-6 max-w-2xl mx-auto">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6 text-center">Registration Details</h2>

                            <div className="space-y-6">
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Asset Title</label>
                                    <input
                                        type="text"
                                        value={title}
                                        onChange={(e) => setTitle(e.target.value)}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-purple focus:ring-2 focus:ring-brand-purple/20 outline-none transition-all font-bold text-slate-900"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Description</label>
                                    <textarea
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        rows={3}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-purple focus:ring-2 focus:ring-brand-purple/20 outline-none transition-all text-slate-600 resize-none"
                                        placeholder="Describe your asset..."
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-bold text-slate-700 mb-2">License Type</label>
                                        <select
                                            value={licenseType}
                                            onChange={(e) => setLicenseType(e.target.value)}
                                            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-purple focus:ring-2 focus:ring-brand-purple/20 outline-none transition-all bg-white"
                                        >
                                            <option value="commercial">Commercial Use</option>
                                            <option value="non-commercial">Non-Commercial</option>
                                            <option value="remix-only">Remix Only</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-bold text-slate-700 mb-2">Royalty (%)</label>
                                        <input
                                            type="number"
                                            value={royalty}
                                            onChange={(e) => setRoyalty(e.target.value)}
                                            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-brand-purple focus:ring-2 focus:ring-brand-purple/20 outline-none transition-all"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-sm font-bold text-slate-700 mb-2">Listing Price (Credits)</label>
                                    <div className="relative">
                                        <FaCoins className="absolute left-4 top-1/2 -translate-y-1/2 text-brand-yellow" />
                                        <input
                                            type="number"
                                            value={price}
                                            onChange={(e) => setPrice(e.target.value)}
                                            className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:border-brand-purple focus:ring-2 focus:ring-brand-purple/20 outline-none transition-all font-bold text-slate-900"
                                        />
                                    </div>
                                </div>

                                <div className="pt-6 flex justify-end gap-4">
                                    <button onClick={() => setStep(2)} className="px-6 py-3 text-slate-500 font-bold hover:text-slate-700">
                                        Back
                                    </button>
                                    <button
                                        onClick={handleRegister}
                                        className="px-8 py-3 bg-brand-purple text-white font-bold rounded-full hover:bg-brand-purple/90 transition-colors inline-flex items-center gap-2 shadow-lg hover:shadow-brand-purple/25"
                                    >
                                        <FaFileContract /> Register on Blockchain
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Step 4: Success */}
                    {step === 4 && (
                        <div className="text-center py-10 animate-in fade-in zoom-in duration-500">
                            <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 text-green-500">
                                <FaCheckCircle size={48} />
                            </div>
                            <h2 className="text-3xl font-black text-slate-900 mb-4">Registration Successful!</h2>
                            <p className="text-slate-500 mb-8 max-w-md mx-auto">
                                <strong>{title}</strong> has been successfully registered on the Story Protocol blockchain and listed on the marketplace.
                            </p>

                            <div className="bg-slate-50 rounded-2xl p-6 max-w-md mx-auto mb-8 text-left border border-slate-200">
                                <div className="flex justify-between mb-2">
                                    <span className="text-slate-500 text-sm">Transaction Hash</span>
                                    <span className="font-mono text-xs text-brand-purple bg-brand-purple/10 px-2 py-1 rounded">0x7f...3a2b</span>
                                </div>
                                <div className="flex justify-between mb-2">
                                    <span className="text-slate-500 text-sm">License Type</span>
                                    <span className="font-bold text-slate-900 capitalize">{licenseType}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-slate-500 text-sm">Listing Price</span>
                                    <span className="font-bold text-slate-900 flex items-center gap-1"><FaCoins className="text-brand-yellow text-xs" /> {price}</span>
                                </div>
                            </div>

                            <div className="flex justify-center gap-4">
                                <Link href="/library" className="px-6 py-3 bg-slate-100 text-slate-700 font-bold rounded-full hover:bg-slate-200 transition-colors">
                                    View in Library
                                </Link>
                                <Link href="/marketplace" className="px-6 py-3 bg-brand-purple text-white font-bold rounded-full hover:bg-brand-purple/90 transition-colors">
                                    View on Marketplace
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}
