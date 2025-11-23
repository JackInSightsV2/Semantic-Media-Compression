'use client';

import React, { useState, useRef, useEffect } from 'react';
import { FaCoins, FaBars, FaUserCircle, FaRedo, FaSignOutAlt } from 'react-icons/fa';
import Link from 'next/link';

export default function UserMenu() {
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    // Close menu when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <div className="relative" ref={menuRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-3 bg-white border border-slate-200 rounded-full pl-2 pr-4 py-2 shadow-sm hover:shadow-md transition-all hover:border-brand-pink group"
            >
                {/* Profile Picture */}
                <div className="w-8 h-8 rounded-full bg-slate-200 overflow-hidden border border-slate-100">
                    <img
                        src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                        alt="User Profile"
                        className="w-full h-full object-cover"
                    />
                </div>

                {/* Credits */}
                <div className="flex items-center gap-1 text-sm font-bold text-slate-700">
                    <FaCoins className="text-brand-yellow" />
                    <span>450C</span>
                </div>

                {/* Divider */}
                <div className="w-px h-4 bg-slate-200 mx-1"></div>

                {/* Hamburger */}
                <FaBars className={`text-slate-400 group-hover:text-slate-600 transition-colors ${isOpen ? 'text-brand-pink' : ''}`} />
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
                    <div className="p-4 border-b border-slate-100 bg-slate-50">
                        <p className="text-sm font-bold text-slate-900">Jack InSights</p>
                        <p className="text-xs text-slate-500 truncate">jack@semantical.ink</p>
                    </div>
                    <div className="p-2">
                        <button className="w-full text-left px-4 py-2 text-sm font-bold text-slate-600 hover:bg-slate-50 hover:text-brand-pink rounded-xl flex items-center gap-3 transition-colors">
                            <FaUserCircle /> View Account
                        </button>
                        <button className="w-full text-left px-4 py-2 text-sm font-bold text-slate-600 hover:bg-slate-50 hover:text-brand-cyan rounded-xl flex items-center gap-3 transition-colors">
                            <FaRedo /> Reload Credits
                        </button>
                    </div>
                    <div className="border-t border-slate-100 p-2">
                        <button className="w-full text-left px-4 py-2 text-xs font-bold text-red-500 hover:bg-red-50 rounded-xl flex items-center gap-3 transition-colors">
                            <FaSignOutAlt /> Sign Out
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
