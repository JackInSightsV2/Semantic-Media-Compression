'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FaHome, FaLayerGroup, FaStore, FaMagic, FaCog, FaSignOutAlt, FaFileContract } from 'react-icons/fa';

interface DashboardLayoutProps {
    children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
    const pathname = usePathname();

    const navItems = [
        { name: 'Explore', path: '/marketplace', icon: FaStore },
        { name: 'Create', path: '/produce', icon: FaMagic },
        { name: 'Register', path: '/register', icon: FaFileContract },
        { name: 'Organize', path: '/library', icon: FaLayerGroup },
    ];

    return (
        <div className="min-h-screen bg-[#fdfdfd] text-slate-900 flex font-sans">
            {/* Sidebar */}
            <aside className="w-64 border-r border-slate-200 flex flex-col fixed h-full bg-white z-10">
                <div className="p-8">
                    <h1 className="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-brand-pink to-brand-cyan">
                        Semantical.Ink
                    </h1>
                </div>

                <nav className="flex-1 px-4 space-y-2">
                    {navItems.map((item) => {
                        const isActive = pathname === item.path || pathname?.startsWith(item.path + '/');
                        return (
                            <Link
                                key={item.path}
                                href={item.path}
                                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-slate-100 text-slate-900 font-bold'
                                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                                    }`}
                            >
                                <item.icon className={isActive ? 'text-brand-pink' : ''} />
                                {item.name}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-slate-100 space-y-2">
                    <button className="flex items-center gap-3 px-4 py-3 w-full text-left text-slate-500 hover:text-slate-900 rounded-xl hover:bg-slate-50 transition-colors">
                        <FaCog />
                        Settings
                    </button>
                    <button className="flex items-center gap-3 px-4 py-3 w-full text-left text-slate-500 hover:text-red-500 rounded-xl hover:bg-slate-50 transition-colors">
                        <FaSignOutAlt />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-64 p-8 overflow-y-auto">
                <div className="max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default DashboardLayout;
