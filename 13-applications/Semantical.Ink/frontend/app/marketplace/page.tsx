'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import MarketplaceCard from '@/components/marketplace/MarketplaceCard';
import { mockMarketplaceListings } from '@/app/data/mockData';
import { FaSearch, FaFilter, FaFire, FaClock, FaCoins } from 'react-icons/fa';

export default function MarketplacePage() {
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  const filteredListings = mockMarketplaceListings.filter(listing => {
    const matchesFilter = filter === 'all' || listing.type === filter; // Simplified filter for now
    const matchesSearch = listing.title.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-8">
        {/* Header */}
        <div className="text-center py-10 relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-brand-pink/10 blur-[100px] rounded-full pointer-events-none" />
          <h1 className="text-5xl md:text-7xl font-black text-slate-900 mb-4 relative z-10">
            Explore <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-pink to-brand-yellow">Gallery</span>
          </h1>
          <p className="text-xl text-slate-500 max-w-2xl mx-auto relative z-10">
            Discover, license, and remix Semantic Blueprints from the world's best creators.
          </p>
        </div>

        {/* Filters & Search */}
        <div className="flex flex-col md:flex-row gap-4 bg-white/80 border border-slate-200 p-4 rounded-2xl backdrop-blur-md sticky top-0 z-20 shadow-sm">
          <div className="relative flex-1">
            <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search for blueprints, genres, or creators..."
              className="w-full bg-slate-50 border border-slate-200 rounded-xl py-3 pl-12 pr-4 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-brand-pink transition-colors"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="flex gap-2">
            <button className="px-4 py-2 rounded-xl bg-brand-pink text-white font-bold flex items-center gap-2">
              <FaFire /> Popular
            </button>
            <button className="px-4 py-2 rounded-xl bg-slate-50 text-slate-500 font-bold hover:text-slate-900 hover:bg-slate-100 flex items-center gap-2 transition-colors">
              <FaClock /> Newest
            </button>
            <button className="px-4 py-2 rounded-xl bg-slate-50 text-slate-500 font-bold hover:text-slate-900 hover:bg-slate-100 flex items-center gap-2 transition-colors">
              <FaCoins /> Price
            </button>
          </div>
        </div>

        {/* Listings Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {filteredListings.map((listing) => (
            <MarketplaceCard key={listing.id} listing={listing} />
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
