
'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import { mockAssets } from '@/app/data/mockData';
import { FaArrowLeft, FaShareAlt, FaShieldAlt, FaCode, FaSitemap, FaStore, FaEdit } from 'react-icons/fa';
import Link from 'next/link';

export default function AssetDetailPage() {
    const params = useParams();
    const id = params?.id as string;
    const asset = mockAssets.find(a => a.id === id);
    const [activeTab, setActiveTab] = useState('overview');

    if (!asset) {
        return (
            <DashboardLayout>
                <div className="text-center py-20">
                    <h2 className="text-2xl font-bold text-white">Asset not found</h2>
                    <Link href="/library" className="text-brand-cyan hover:underline mt-4 inline-block">
                        Return to Library
                    </Link>
                </div>
            </DashboardLayout>
        );
    }

    const tabs = [
        { id: 'overview', label: 'Overview', icon: FaEdit },
        { id: 'blueprint', label: 'The Blueprint', icon: FaCode },
        { id: 'genealogy', label: 'Genealogy', icon: FaSitemap },
        { id: 'marketplace', label: 'Marketplace', icon: FaStore },
        { id: 'protection', label: 'Protection', icon: FaShieldAlt },
    ];

    return (
        <DashboardLayout>
            <div className="max-w-5xl mx-auto">
                {/* Back Link */}
                <Link href="/library" className="inline-flex items-center gap-2 text-slate-400 hover:text-white mb-6 transition-colors">
                    <FaArrowLeft /> Back to Library
                </Link>

                {/* Header */}
                <div className="flex flex-col md:flex-row gap-8 mb-10">
                    <div className="w-full md:w-64 h-64 rounded-3xl overflow-hidden shadow-2xl shrink-0">
                        <img src={asset.thumbnailUrl} alt={asset.title} className="w-full h-full object-cover" />
                    </div>

                    <div className="flex-1">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <div className="flex items-center gap-3 mb-2">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold border ${asset.type === 'original'
                                            ? 'bg-brand-purple/20 text-brand-purple border-brand-purple/30'
                                            : 'bg-brand-cyan/20 text-brand-cyan border-brand-cyan/30'
                                        }`}>
                                        {asset.type.toUpperCase()}
                                    </span>
                                    <span className="text-slate-500 text-sm font-bold uppercase tracking-wider">
                                        {asset.format}
                                    </span>
                                </div>
                                <h1 className="text-5xl font-black text-white mb-4">{asset.title}</h1>
                            </div>

                            <div className="flex gap-2">
                                <button className="p-3 rounded-full bg-white/5 hover:bg-white/10 text-white border border-white/10 transition-colors">
                                    <FaShareAlt />
                                </button>
                            </div>
                        </div>

                        <p className="text-slate-300 text-lg mb-6 leading-relaxed">
                            {asset.description}
                        </p>

                        <div className="flex gap-4">
                            <button className="px-8 py-3 bg-brand-pink hover:bg-brand-pink/90 text-white font-bold rounded-full transition-all hover:shadow-lg hover:shadow-brand-pink/20">
                                Generate Derivative
                            </button>
                            <button className="px-8 py-3 bg-white/5 hover:bg-white/10 text-white font-bold rounded-full border border-white/10 transition-colors">
                                View on Story Protocol
                            </button>
                        </div>
                    </div>
                </div>

                {/* Tabs */}
                <div className="border-b border-white/10 mb-8">
                    <div className="flex gap-8 overflow-x-auto">
                        {tabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`pb-4 px-2 font-bold flex items-center gap-2 transition-colors relative ${activeTab === tab.id
                                        ? 'text-brand-cyan'
                                        : 'text-slate-500 hover:text-slate-300'
                                    }`}
                            >
                                <tab.icon />
                                {tab.label}
                                {activeTab === tab.id && (
                                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-cyan shadow-[0_0_10px_rgba(6,182,212,0.5)]" />
                                )}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Tab Content */}
                <div className="min-h-[400px]">
                    {activeTab === 'overview' && (
                        <div className="grid grid-cols-2 gap-8">
                            <div className="bg-brand-dark border border-white/10 rounded-3xl p-8">
                                <h3 className="text-xl font-bold text-white mb-4">Metadata</h3>
                                <div className="space-y-4">
                                    <div className="flex justify-between py-2 border-b border-white/5">
                                        <span className="text-slate-500">Created</span>
                                        <span className="text-white">{new Date(asset.createdAt).toLocaleDateString()}</span>
                                    </div>
                                    <div className="flex justify-between py-2 border-b border-white/5">
                                        <span className="text-slate-500">Status</span>
                                        <span className="text-white capitalize">{asset.status}</span>
                                    </div>
                                    <div className="flex justify-between py-2 border-b border-white/5">
                                        <span className="text-slate-500">Story Protocol ID</span>
                                        <span className="text-brand-cyan font-mono text-sm">{asset.storyProtocolId || 'Pending'}</span>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-brand-dark border border-white/10 rounded-3xl p-8">
                                <h3 className="text-xl font-bold text-white mb-4">Tags</h3>
                                <div className="flex flex-wrap gap-2">
                                    {asset.tags?.map(tag => (
                                        <span key={tag} className="px-3 py-1 bg-white/5 rounded-full text-slate-300 text-sm border border-white/10">
                                            #{tag}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'blueprint' && (
                        <div className="bg-[#0d1117] rounded-3xl p-6 border border-white/10 font-mono text-sm overflow-hidden">
                            <div className="flex items-center gap-2 mb-4 text-slate-500 border-b border-white/5 pb-4">
                                <div className="w-3 h-3 rounded-full bg-red-500" />
                                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                                <div className="w-3 h-3 rounded-full bg-green-500" />
                                <span className="ml-2">semantic-blueprint.json</span>
                            </div>
                            <pre className="text-blue-300 overflow-x-auto">
                                {`{
  "meta": {
    "title": "${asset.title}",
    "version": "1.0.0",
    "fingerprint": "0x8f2...a91"
  },
  "narrative": {
    "arcs": [
      {
        "id": "arc_1",
        "type": "hero_journey",
        "intensity": 0.85
      }
    ],
    "themes": ${JSON.stringify(asset.tags, null, 4)}
  },
  "characters": [
    {
      "name": "Protagonist",
      "archetype": "The Explorer",
      "traits": ["brave", "curious", "isolated"]
    }
  ]
}`}
                            </pre>
                        </div>
                    )}

                    {activeTab === 'genealogy' && (
                        <div className="bg-brand-dark border border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center min-h-[400px] relative overflow-hidden">
                            <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(#4C1D95 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
                            <div className="relative z-10 flex flex-col items-center gap-8">
                                {/* Parent */}
                                {asset.parentId && (
                                    <div className="flex flex-col items-center gap-2 opacity-50">
                                        <div className="w-16 h-16 rounded-full bg-slate-700 border-2 border-slate-500"></div>
                                        <span className="text-slate-500 text-sm">Parent Asset</span>
                                        <div className="h-8 w-0.5 bg-slate-500"></div>
                                    </div>
                                )}

                                {/* Current */}
                                <div className="p-1 rounded-full bg-gradient-to-r from-brand-pink to-brand-cyan shadow-[0_0_30px_rgba(236,72,153,0.3)]">
                                    <div className="w-24 h-24 rounded-full bg-brand-dark border-4 border-brand-dark overflow-hidden">
                                        <img src={asset.thumbnailUrl} className="w-full h-full object-cover" />
                                    </div>
                                </div>
                                <span className="font-bold text-white bg-brand-dark px-4 py-1 rounded-full border border-white/10">
                                    {asset.title}
                                </span>

                                {/* Children */}
                                <div className="flex flex-col items-center gap-2">
                                    <div className="h-8 w-0.5 bg-brand-cyan"></div>
                                    <div className="flex gap-8">
                                        <div className="w-12 h-12 rounded-full bg-brand-cyan/20 border border-brand-cyan flex items-center justify-center text-brand-cyan text-xs font-bold">
                                            +
                                        </div>
                                    </div>
                                    <span className="text-brand-cyan text-sm">Create Derivative</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'marketplace' && (
                        <div className="bg-brand-dark border border-white/10 rounded-3xl p-8 text-center">
                            <div className="w-16 h-16 bg-brand-yellow/10 rounded-full flex items-center justify-center mx-auto mb-4 text-brand-yellow">
                                <FaStore size={32} />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-2">List on Marketplace</h3>
                            <p className="text-slate-400 max-w-md mx-auto mb-8">
                                Allow other creators to remix your work. You earn royalties for every derivative created.
                            </p>
                            <button className="px-8 py-3 bg-brand-yellow text-brand-dark font-bold rounded-full hover:bg-brand-yellow/90 transition-colors">
                                Configure Listing
                            </button>
                        </div>
                    )}

                    {activeTab === 'protection' && (
                        <div className="space-y-4">
                            <div className="bg-brand-dark border border-white/10 rounded-3xl p-6 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center text-green-500">
                                        <FaShieldAlt size={24} />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white">Story Protocol Registration</h4>
                                        <p className="text-slate-400 text-sm">Asset is fully registered and protected on-chain.</p>
                                    </div>
                                </div>
                                <span className="text-green-500 font-bold text-sm">ACTIVE</span>
                            </div>

                            <div className="bg-brand-dark border border-white/10 rounded-3xl p-6">
                                <h4 className="font-bold text-white mb-4">Infringement Scans</h4>
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                                        <div className="flex items-center gap-3">
                                            <div className="w-2 h-2 rounded-full bg-green-500"></div>
                                            <span className="text-slate-300">Scan #1023 - Web Crawl</span>
                                        </div>
                                        <span className="text-slate-500 text-sm">Today, 10:00 AM</span>
                                    </div>
                                    <div className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-brand-yellow/30">
                                        <div className="flex items-center gap-3">
                                            <div className="w-2 h-2 rounded-full bg-brand-yellow animate-pulse"></div>
                                            <span className="text-white font-bold">Scan #1022 - YouTube Match Found</span>
                                        </div>
                                        <button className="text-brand-yellow text-sm font-bold hover:underline">Review Match</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}
