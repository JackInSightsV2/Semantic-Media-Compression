'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import AssetCard from '@/components/library/AssetCard';
import { mockAssets } from '@/app/data/mockData';
import { FaSearch, FaFilter, FaPlus, FaLayerGroup } from 'react-icons/fa';
import Link from 'next/link';

export default function LibraryPage() {
    const [filter, setFilter] = useState('all');
    const [search, setSearch] = useState('');

    const filteredAssets = mockAssets.filter(asset => {
        const matchesFilter = filter === 'all' || asset.type === filter;
        const matchesSearch = asset.title.toLowerCase().includes(search.toLowerCase());
        return matchesFilter && matchesSearch;
    });

    return (
        <DashboardLayout>
            <div className="flex flex-col gap-8">
                {/* Hero Header */}
                <div className="text-center py-10 relative">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-brand-cyan/10 blur-[100px] rounded-full pointer-events-none" />
                    <h1 className="text-5xl md:text-7xl font-black text-slate-900 mb-4 relative z-10">
                        Organize <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-cyan to-brand-purple">Library</span>
                    </h1>
                    <p className="text-xl text-slate-500 max-w-2xl mx-auto relative z-10">
                        Manage your registered Intellectual Property and derivatives.
                    </p>

                    <div className="mt-8 relative z-10">
                        <Link
                            href="/produce"
                            className="px-8 py-3 bg-slate-900 text-white font-bold rounded-full hover:bg-slate-800 transition-all inline-flex items-center gap-2 shadow-lg hover:shadow-xl hover:-translate-y-1"
                        >
                            <FaPlus /> Create New Blueprint
                        </Link>
                    </div>
                </div>

                {/* Filters & Search */}
                <div className="flex flex-col md:flex-row gap-4 bg-white/80 border border-slate-200 p-4 rounded-2xl backdrop-blur-md sticky top-0 z-20 shadow-sm">
                    <div className="relative flex-1">
                        <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Search your assets..."
                            className="w-full bg-slate-50 border border-slate-200 rounded-xl py-3 pl-12 pr-4 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-brand-cyan transition-colors"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0">
                        {['all', 'original', 'derivative'].map((type) => (
                            <button
                                key={type}
                                onClick={() => setFilter(type)}
                                className={`px-6 py-3 rounded-xl font-bold capitalize whitespace-nowrap transition-colors ${filter === type
                                        ? 'bg-brand-cyan text-white'
                                        : 'bg-slate-50 text-slate-500 hover:text-slate-900 hover:bg-slate-100'
                                    }`}
                            >
                                {type}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Asset Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {filteredAssets.map((asset) => (
                        <AssetCard key={asset.id} asset={asset} />
                    ))}

                    {/* Empty State */}
                    {filteredAssets.length === 0 && (
                        <div className="col-span-full py-20 text-center border-2 border-dashed border-slate-200 rounded-3xl">
                            <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-300">
                                <FaLayerGroup size={24} />
                            </div>
                            <p className="text-slate-400 font-bold">No assets found matching your criteria.</p>
                            <button
                                onClick={() => { setFilter('all'); setSearch('') }}
                                className="mt-2 text-brand-cyan font-bold hover:underline"
                            >
                                Clear filters
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}
