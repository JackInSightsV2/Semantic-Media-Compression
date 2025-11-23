'use client';

import React from 'react';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import UserStatusCard from '@/components/dashboard/UserStatusCard';
import QuickActions from '@/components/dashboard/QuickActions';
import ActivityFeed from '@/components/dashboard/ActivityFeed';
import { mockActivities } from '@/app/data/mockData';
import { FaChartLine, FaLayerGroup, FaCoins } from 'react-icons/fa';

export default function DashboardPage() {
    return (
        <DashboardLayout>
            <div className="grid grid-cols-12 gap-8">
                {/* Header Section */}
                <div className="col-span-12 mb-4">
                    <h2 className="text-4xl font-black text-slate-900 mb-2">Dashboard</h2>
                    <p className="text-slate-500">Overview of your creative ecosystem.</p>
                </div>

                {/* Top Row: Status & Quick Actions */}
                <div className="col-span-12 lg:col-span-4 h-80">
                    <UserStatusCard />
                </div>
                <div className="col-span-12 lg:col-span-8 h-80">
                    <QuickActions />
                </div>

                {/* Middle Row: Analytics & Activity */}
                <div className="col-span-12 lg:col-span-8 h-96">
                    <ActivityFeed activities={mockActivities} />
                </div>

                <div className="col-span-12 lg:col-span-4 h-96 flex flex-col gap-4">
                    {/* Analytics Mini-Cards */}
                    <div className="bg-white border border-slate-200 rounded-3xl p-6 flex-1 flex flex-col justify-center relative overflow-hidden shadow-sm">
                        <div className="absolute right-0 top-0 p-4 opacity-5">
                            <FaLayerGroup size={80} className="text-brand-cyan" />
                        </div>
                        <span className="text-slate-400 text-sm font-bold uppercase">IP Reach</span>
                        <div className="flex items-baseline gap-2">
                            <span className="text-4xl font-black text-slate-900">1,240</span>
                            <span className="text-brand-cyan text-sm font-bold flex items-center gap-1">
                                <FaChartLine /> +12%
                            </span>
                        </div>
                        <p className="text-slate-500 text-xs mt-2">Derivatives created from your work</p>
                    </div>

                    <div className="bg-white border border-slate-200 rounded-3xl p-6 flex-1 flex flex-col justify-center relative overflow-hidden shadow-sm">
                        <div className="absolute right-0 top-0 p-4 opacity-5">
                            <FaCoins size={80} className="text-brand-yellow" />
                        </div>
                        <span className="text-slate-400 text-sm font-bold uppercase">Earnings</span>
                        <div className="flex items-baseline gap-2">
                            <span className="text-4xl font-black text-slate-900">$450.00</span>
                            <span className="text-brand-yellow text-sm font-bold flex items-center gap-1">
                                <FaChartLine /> +5%
                            </span>
                        </div>
                        <p className="text-slate-500 text-xs mt-2">Revenue this month</p>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
