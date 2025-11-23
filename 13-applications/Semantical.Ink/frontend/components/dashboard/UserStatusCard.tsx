
import React from 'react';

const UserStatusCard = () => {
    return (
        <div className="bg-white border border-slate-200 rounded-3xl p-6 flex flex-col justify-between h-full relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
            {/* Background Glow */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-brand-pink/10 blur-[60px] rounded-full -mr-10 -mt-10 pointer-events-none" />

            <div>
                <h2 className="text-slate-500 text-sm font-bold uppercase tracking-wide mb-1">Welcome back</h2>
                <h3 className="text-3xl font-black text-slate-900 mb-4">Alex Creator</h3>

                <div className="flex items-center gap-2 mb-6">
                    <span className="px-3 py-1 rounded-full bg-brand-purple/10 text-brand-purple text-xs font-bold border border-brand-purple/20">
                        PRO CREATOR
                    </span>
                </div>
            </div>

            <div className="mt-auto">
                <div className="flex justify-between items-end mb-2">
                    <span className="text-slate-500 text-sm">Credit Balance</span>
                    <span className="text-2xl font-bold text-brand-yellow drop-shadow-sm">150 CR</span>
                </div>
                <button className="w-full py-3 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-slate-900 font-bold transition-all text-sm">
                    Buy More Credits
                </button>
            </div>
        </div>
    );
};

export default UserStatusCard;
