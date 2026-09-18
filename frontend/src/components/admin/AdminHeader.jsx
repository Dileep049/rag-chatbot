import React from 'react';
import { RefreshCw, MessageSquare, LogOut, ShieldCheck } from 'lucide-react';
import { useAuth } from '../../auth/AuthContext';

export default function AdminHeader({ onRefresh, loading, onReturnToChat }) {
  const { logout, user } = useAuth();

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-30 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-xl shadow-lg shadow-indigo-600/30 shrink-0">
              🇮🇳
            </div>
            <div>
              <h1 className="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                Citizen Assistance AI
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Admin Dashboard
                </span>
                <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                  DEMO MODE: ON
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                Official Knowledge Base • Logged in as <strong className="text-slate-200 font-semibold">{user?.email || 'Admin'}</strong>
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2.5">
            <button
              onClick={onRefresh}
              disabled={loading}
              className="flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs sm:text-sm font-medium border border-slate-700 transition"
            >
              <RefreshCw className={`w-4 h-4 text-indigo-400 ${loading ? 'animate-spin' : ''}`} />
              <span className="hidden sm:inline">Refresh</span>
            </button>

            <button
              onClick={onReturnToChat}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-medium border border-slate-700 transition"
            >
              <MessageSquare className="w-4 h-4 text-indigo-400" />
              <span>Chat</span>
            </button>

            <button
              onClick={logout}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 text-xs sm:text-sm font-medium border border-rose-800/50 transition"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
