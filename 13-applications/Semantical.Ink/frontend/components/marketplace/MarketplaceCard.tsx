
import React from 'react';
import Link from 'next/link';
import { MarketplaceListing } from '@/app/data/mockData';
import { FaPalette, FaBook, FaFilm, FaHeadphones, FaCoins, FaCodeBranch } from 'react-icons/fa';

interface MarketplaceCardProps {
    listing: MarketplaceListing;
}

const MarketplaceCard: React.FC<MarketplaceCardProps> = ({ listing }) => {
    const getIcon = (format: MarketplaceListing['format']) => {
        switch (format) {
            case 'novel': return <FaBook />;
            case 'script': return <FaFilm />;
            case 'audio': return <FaHeadphones />;
            case 'comic': return <FaPalette />;
            default: return <FaBook />;
        }
    };

    return (
        <div className="group bg-white border border-slate-200 rounded-3xl overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            {/* Thumbnail */}
            <div className="relative h-56 overflow-hidden">
                <img
                    src={listing.thumbnailUrl}
                    alt={listing.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                <div className="absolute bottom-4 left-4 right-4 translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300">
                    <Link
                        href={`/marketplace/${listing.id}`}
                        className="block w-full py-2 bg-brand-pink text-white text-center font-bold rounded-full shadow-lg hover:bg-brand-pink/90 transition-colors"
                    >
                        View Blueprint
                    </Link>
                </div>
            </div>

            {/* Content */}
            <div className="p-5">
                <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-2">
                        <img
                            src={listing.authorAvatar}
                            alt={listing.author}
                            className="w-6 h-6 rounded-full border border-slate-200"
                        />
                        <span className="text-xs font-bold text-slate-600">{listing.author}</span>
                    </div>
                    <div className="flex items-center gap-1 text-xs font-bold text-slate-400 uppercase tracking-wider">
                        {getIcon(listing.format)}
                        <span>{listing.format}</span>
                    </div>
                </div>

                <Link href={`/marketplace/${listing.id}`} className="block">
                    <h3 className="text-xl font-bold text-slate-900 mb-1 group-hover:text-brand-pink transition-colors line-clamp-1">
                        {listing.title}
                    </h3>
                </Link>

                <div className="flex flex-wrap gap-2 mb-4">
                    {listing.tags?.slice(0, 3).map(tag => (
                        <span key={tag} className="text-[10px] font-bold px-2 py-1 bg-slate-100 text-slate-500 rounded-full">
                            #{tag}
                        </span>
                    ))}
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-1 text-brand-dark font-black text-lg">
                        <FaCoins className="text-brand-yellow" />
                        {listing.priceCredits}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-slate-500 font-medium">
                        <FaCodeBranch />
                        {listing.derivativeCount} Remixes
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MarketplaceCard;
