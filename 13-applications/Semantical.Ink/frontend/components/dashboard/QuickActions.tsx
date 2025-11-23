import React from 'react';
import Link from 'next/link';
import { FaPlus, FaSearch, FaFingerprint, FaFileContract, FaQuestionCircle } from 'react-icons/fa';

const QuickActions = () => {
    const actions = [
        {
            label: 'New Blueprint',
            icon: FaPlus,
            href: '/produce',
            color: 'bg-brand-pink',
            textColor: 'text-white',
            description: 'Create a new Semantic Blueprint from your files.',
        },
        {
            label: 'Scan IP',
            icon: FaSearch,
            href: '/library?action=scan',
            color: 'bg-brand-cyan/10',
            textColor: 'text-brand-cyan',
            description: 'Check the web for potential infringement of your IP.',
        },
        {
            label: 'Register IP',
            icon: FaFingerprint,
            href: '/register',
            color: 'bg-brand-purple/10',
            textColor: 'text-brand-purple',
            description: 'Register your work on the Story Protocol blockchain.',
        },
        {
            label: 'Update Contract',
            icon: FaFileContract,
            href: '/register?action=contract',
            color: 'bg-brand-yellow/10',
            textColor: 'text-brand-yellow',
            description: 'Modify licensing terms and royalty settings.',
        },
    ];

    return (
        <div className="grid grid-cols-2 gap-4 h-full">
            {actions.map((action) => (
                <div key={action.label} className="relative group h-full">
                    <Link
                        href={action.href}
                        className={`flex flex-col items-center justify-center h-full p-4 rounded-2xl border transition-all hover:-translate-y-1 hover:shadow-lg ${action.label === 'New Blueprint'
                                ? 'bg-brand-pink hover:bg-brand-pink/90 border-transparent shadow-brand-pink/20'
                                : 'bg-white border-slate-200 hover:border-brand-pink/50 shadow-sm'
                            }`}
                    >
                        <div className={`p-3 rounded-full mb-2 ${action.label === 'New Blueprint' ? 'bg-white/20 text-white' : `${action.color} ${action.textColor}`}`}>
                            <action.icon size={20} />
                        </div>
                        <span className={`text-sm font-bold ${action.label === 'New Blueprint' ? 'text-white' : 'text-slate-700'}`}>
                            {action.label}
                        </span>
                    </Link>

                    {/* Tooltip Icon */}
                    <div className="absolute top-3 right-3 group/tooltip">
                        <FaQuestionCircle className={`${action.label === 'New Blueprint' ? 'text-white/50 hover:text-white' : 'text-slate-300 hover:text-slate-500'} transition-colors cursor-help`} />

                        {/* Tooltip Content */}
                        <div className="absolute bottom-full right-0 mb-2 w-48 p-3 bg-slate-800 text-white text-xs rounded-xl shadow-xl opacity-0 invisible group-hover/tooltip:opacity-100 group-hover/tooltip:visible transition-all z-20 pointer-events-none">
                            {action.description}
                            <div className="absolute bottom-[-4px] right-1 w-2 h-2 bg-slate-800 rotate-45" />
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default QuickActions;
