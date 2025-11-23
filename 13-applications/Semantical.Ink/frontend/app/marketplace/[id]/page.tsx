
'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import { mockMarketplaceListings } from '@/app/data/mockData';
import { FaArrowLeft, FaCoins, FaCodeBranch, FaShieldAlt, FaStar, FaShareAlt } from 'react-icons/fa';
import Link from 'next/link';

export default function MarketplaceListingPage() {
    const params = useParams();
    const id = params?.id as string;
    const listing = mockMarketplaceListings.find(l => l.id === id);

    if (!listing) {
        return (
            <DashboardLayout>
                <div className="text-center py-20">
                    <h2 className="text-2xl font-bold text-white">Listing not found</h2>
                    <Link href="/marketplace" className="text-brand-pink hover:underline mt-4 inline-block">
                        Return to Marketplace
                    </Link>
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="max-w-6xl mx-auto">
                {/* Back Link */}
                <Link href="/marketplace" className="inline-flex items-center gap-2 text-slate-400 hover:text-white mb-6 transition-colors">
                    <FaArrowLeft /> Back to Marketplace
                </Link>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                    {/* Left Column: Media */}
                    <div className="lg:col-span-7 space-y-8">
                        <div className="rounded-3xl overflow-hidden shadow-2xl border border-white/10 relative group">
                            <img src={listing.thumbnailUrl} alt={listing.title} className="w-full h-auto object-cover" />
                            <div className="absolute inset-0 bg-gradient-to-t from-brand-dark/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-8">
                                <button className="p-4 rounded-full bg-white/10 backdrop-blur-md text-white hover:bg-white/20 transition-colors">
                                    <FaShareAlt size={24} />
                                </button>
                            </div>
                        </div>

                        {/* Semantic Preview (Mock) */}
                        <div className="bg-brand-dark border border-white/10 rounded-3xl p-8">
                            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <FaCodeBranch className="text-brand-cyan" />
                                Semantic Fingerprint Preview
                            </h3>
                            <div className="h-48 bg-[#0d1117] rounded-xl p-4 font-mono text-xs text-blue-300 overflow-hidden relative">
                                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#0d1117]" />
                                <pre>
                                    {`{
  "fingerprint": "${listing.storyProtocolId}",
  "narrative_structure": {
    "archetype": "Hero's Journey",
    "pacing": "Fast",
    "tone": "Dark/Gritty"
  },
  "entities": [
    "Protagonist",
    "Antagonist",
    "MacGuffin"
  ]
}`}
                                </pre>
                                <div className="absolute bottom-4 left-1/2 -translate-x-1/2">
                                    <span className="px-4 py-2 bg-white/10 backdrop-blur-md rounded-full text-white text-xs font-bold">
                                        Purchase to view full blueprint
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Details & Purchase */}
                    <div className="lg:col-span-5 space-y-8">
                        <div>
                            <div className="flex items-center gap-3 mb-4">
                                <img src={listing.authorAvatar} alt={listing.author} className="w-10 h-10 rounded-full border-2 border-brand-pink" />
                                <div>
                                    <p className="text-slate-400 text-xs font-bold uppercase">Created By</p>
                                    <p className="text-white font-bold">{listing.author}</p>
                                </div>
                            </div>

                            <h1 className="text-5xl font-black text-white mb-4 leading-tight">{listing.title}</h1>

                            <div className="flex flex-wrap gap-2 mb-6">
                                {listing.tags?.map(tag => (
                                    <span key={tag} className="px-3 py-1 bg-white/5 rounded-full text-slate-300 text-sm border border-white/10">
                                        #{tag}
                                    </span>
                                ))}
                            </div>

                            <p className="text-slate-300 text-lg leading-relaxed mb-8">
                                {listing.description}
                            </p>

                            <div className="bg-white/5 border border-white/10 rounded-3xl p-6 mb-8">
                                <div className="flex justify-between items-center mb-6">
                                    <span className="text-slate-400 font-bold">Price</span>
                                    <div className="flex items-center gap-2 text-3xl font-black text-white">
                                        <FaCoins className="text-brand-yellow" />
                                        {listing.priceCredits}
                                    </div>
                                </div>

                                <button className="w-full py-4 bg-brand-pink hover:bg-brand-pink/90 text-white font-bold text-lg rounded-full shadow-lg shadow-brand-pink/20 transition-all hover:-translate-y-1 mb-3">
                                    Purchase Blueprint
                                </button>
                                <p className="text-center text-slate-500 text-xs">
                                    Includes commercial license for 1 derivative work.
                                </p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-brand-dark border border-white/10 rounded-2xl p-4 flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-brand-cyan/20 flex items-center justify-center text-brand-cyan">
                                        <FaCodeBranch />
                                    </div>
                                    <div>
                                        <p className="text-white font-bold text-lg">{listing.derivativeCount}</p>
                                        <p className="text-slate-500 text-xs">Remixes</p>
                                    </div>
                                </div>
                                <div className="bg-brand-dark border border-white/10 rounded-2xl p-4 flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center text-green-500">
                                        <FaShieldAlt />
                                    </div>
                                    <div>
                                        <p className="text-white font-bold text-lg">Verified</p>
                                        <p className="text-slate-500 text-xs">Story Protocol</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
