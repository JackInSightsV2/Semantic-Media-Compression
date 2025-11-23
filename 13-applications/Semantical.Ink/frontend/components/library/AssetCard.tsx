import React from 'react';
import Link from 'next/link';
import { Asset } from '@/app/data/mockData';
import { FaBook, FaFilm, FaHeadphones, FaPalette, FaEllipsisV, FaShareAlt } from 'react-icons/fa';

interface AssetCardProps {
    asset: Asset;
}

const AssetCard: React.FC<AssetCardProps> = ({ asset }) => {
    const getIcon = (format: Asset['format']) => {
        switch (format) {
            case 'novel': return <FaBook />;
            case 'script': return <FaFilm />;
            case 'audio': return <FaHeadphones />;
            case 'comic': return <FaPalette />;
            default: return <FaBook />;
        }
    };

    const getStatusColor = (status: Asset['status']) => {
        switch (status) {
            case 'registered': return 'bg-green-500/20 text-green-400 border-green-500/30';
            case 'processing': return 'bg-brand-yellow/20 text-brand-yellow border-brand-yellow/30 animate-pulse';
            case 'draft': return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
            case 'listed': return 'bg-brand-pink/20 text-brand-pink border-brand-pink/30';
            default: return 'bg-slate-500/20 text-slate-400';
        }
    };

    return (
        <div className="group bg-white border border-slate-200 rounded-3xl overflow-hidden hover:border-brand-cyan/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-brand-cyan/5">
            {/* Thumbnail */}
            <div className="relative h-48 overflow-hidden">
                <img
                    src={asset.thumbnailUrl}
                    alt={asset.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                {/* Type Badge */}
                <div className="absolute top-4 left-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold border backdrop-blur-md ${asset.type === 'original'
                        ? 'bg-brand-purple/90 text-white border-brand-purple'
                        : 'bg-brand-cyan/90 text-white border-brand-cyan'
                        }`}>
                        {asset.type.toUpperCase()}
                    </span>
                </div>

                {/* Quick Actions Overlay */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                    <button className="p-2 rounded-full bg-white/20 backdrop-blur-md text-white hover:bg-white/30 transition-colors">
                        <FaShareAlt size={14} />
                    </button>
                    <button className="p-2 rounded-full bg-white/20 backdrop-blur-md text-white hover:bg-white/30 transition-colors">
                        <FaEllipsisV size={14} />
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="p-5">
                <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-wider">
                        {getIcon(asset.format)}
                        <span>{asset.format}</span>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getStatusColor(asset.status)}`}>
                        {asset.status.toUpperCase()}
                    </span>
                </div>

                <Link href={`/library/${asset.id}`} className="block">
                    <h3 className="text-lg font-bold text-slate-900 mb-1 group-hover:text-brand-cyan transition-colors line-clamp-1">
                        {asset.title}
                    </h3>
                </Link>

                <p className="text-slate-500 text-sm line-clamp-2 mb-4 h-10">
                    {asset.description}
                </p>

                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <span className="text-xs text-slate-400">
                        {new Date(asset.createdAt).toLocaleDateString()}
                    </span>
                    {asset.infringementStatus === 'detecting' && (
                        <span className="text-xs text-brand-yellow flex items-center gap-1">
                            <span className="w-2 h-2 rounded-full bg-brand-yellow animate-pulse" />
                            Scanning...
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AssetCard;
