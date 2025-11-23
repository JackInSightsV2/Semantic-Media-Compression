import React from 'react';
import { Activity } from '@/app/data/mockData';
import { FaBell, FaShoppingCart, FaRobot, FaLink, FaExclamationTriangle } from 'react-icons/fa';

interface ActivityFeedProps {
    activities: Activity[];
}

const ActivityFeed: React.FC<ActivityFeedProps> = ({ activities }) => {
    const getIcon = (type: Activity['type']) => {
        switch (type) {
            case 'alert': return <FaExclamationTriangle className="text-red-500" />;
            case 'commerce': return <FaShoppingCart className="text-brand-yellow" />;
            case 'system': return <FaRobot className="text-brand-cyan" />;
            case 'derivative': return <FaLink className="text-brand-pink" />;
            default: return <FaBell className="text-slate-400" />;
        }
    };

    return (
        <div className="bg-white border border-slate-200 rounded-3xl p-6 h-full flex flex-col shadow-sm">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-black text-slate-900">Activity</h3>
                <button className="text-sm font-bold text-brand-pink hover:text-brand-pink/80">View All</button>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 space-y-4 custom-scrollbar">
                {activities.map((activity) => (
                    <div key={activity.id} className="flex gap-4 items-start group cursor-pointer hover:bg-slate-50 p-3 rounded-xl transition-colors">
                        <div className="mt-1 p-2 bg-slate-100 rounded-full group-hover:bg-white group-hover:shadow-sm transition-all">
                            {getIcon(activity.type)}
                        </div>
                        <div className="flex-1">
                            <p className="text-slate-900 font-medium text-sm leading-snug">
                                {activity.message}
                            </p>
                            <span className="text-xs text-slate-400 font-bold mt-1 block">
                                {activity.timestamp}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ActivityFeed;
